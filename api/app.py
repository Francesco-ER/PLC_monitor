# api/app.py
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

# ======== CONFIG PLC ========
PLC_IP   = "192.168.1.10"
PLC_PORT = 502
UNIT_ID  = 1
# ============================

# ======== MAPA (EJEMPLO) =========
Y_TAGS = {   # FC1 - Coils - salidas físicas
    6:  "Y6_VentiladorBajo",
    12: "Y12_Resistencia",
    26: "Y26_BombaAgua",
}
M_TAGS = {   # FC1 - Coils - marcas internas
    130: "M130_MotorAstillas",
    132: "M132_ValvulaHumo",
    32:  "M32_PT_Humado",
}
D_TAGS = {   # FC3 - Holding registers (addr: (nombre, tipo, escala))
    8222: ("Temp_producto",   "INT16", 10.0),
    296: ("SP_Producto", "INT16", 10.0),
}
# Si tus Y/M no son base 0, pon los offsets reales encontrados
Y_BASE = 114
M_BASE = 0
# =================================

app = FastAPI(title="PLC Monitor API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

WEB_DIR = (Path(__file__).resolve().parent.parent / "web")
app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

@app.get("/")
def root_page():
    return FileResponse(str(WEB_DIR / "index.html"))

def _client():
    return ModbusTcpClient(PLC_IP, port=PLC_PORT, timeout=3)

@app.get("/health")
def health():
    c = _client()
    if not c.connect():
        return {"ok": False, "detail": "No conecta TCP"}
    try:
        r = c.read_holding_registers(0, 1, unit=UNIT_ID)
        return {"ok": (not r.isError())}
    finally:
        c.close()

@app.get("/io")
def io():
    c = _client()
    if not c.connect():
        raise HTTPException(503, "PLC no disponible")
    try:
        dataY, dataM = {}, {}

        if Y_TAGS:
            max_y = max(Y_TAGS.keys())
            # lee desde Y_BASE hasta Y_BASE+max_y (incluye huecos)
            rY = c.read_coils(Y_BASE, max_y + 1, unit=UNIT_ID)
            if rY.isError():
                raise HTTPException(502, f"Error lectura Coils Y (base={Y_BASE})")
            for idx, name in Y_TAGS.items():
                if idx < len(rY.bits):
                    dataY[name] = bool(rY.bits[idx])
                else:
                    dataY[name] = None  # fuera de rango leído

        if M_TAGS:
            max_m = max(M_TAGS.keys())
            rM = c.read_coils(M_BASE, max_m + 1, unit=UNIT_ID)
            if rM.isError():
                raise HTTPException(502, f"Error lectura Coils M (base={M_BASE})")
            for idx, name in M_TAGS.items():
                if idx < len(rM.bits):
                    dataM[name] = bool(rM.bits[idx])
                else:
                    dataM[name] = None

        return {"Y": dataY, "M": dataM}
    finally:
        c.close()

@app.get("/tags")
def tags():
    c = _client()
    if not c.connect():
        raise HTTPException(503, "PLC no disponible")
    try:
        out = {}
        for addr, (name, dtype, scale) in D_TAGS.items():
            count = 2 if dtype == "FLOAT32" else 1
            r = c.read_holding_registers(addr, count, unit=UNIT_ID)
            if r.isError():
                raise HTTPException(502, f"Error HR {addr}")
            regs = r.registers
            if dtype == "INT16":
                raw = regs[0]
                val = raw * (1.0/scale)
            elif dtype == "UINT16":
                raw = regs[0] & 0xFFFF
                val = raw * (1.0/scale)
            elif dtype == "FLOAT32":
                dec = BinaryPayloadDecoder.fromRegisters(regs, byteorder=Endian.Big, wordorder=Endian.Big)
                val = dec.decode_32bit_float()
            else:
                val = regs[0]
            out[name] = val
        return out
    finally:
        c.close()
