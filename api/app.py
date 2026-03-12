# api/app.py
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any

app = FastAPI(title="PLC Monitor Cloud")

# ===== Import utilidades cloud =====
try:
    from api.models import IngestPayload
    from api.auth import is_valid
    from api.storage import set_snapshot, get_snapshot
except Exception as e:
    IngestPayload = None
    is_valid = None
    set_snapshot = None
    get_snapshot = None
    print("[WARN] Módulos cloud no disponibles todavía:", e)

# ===== Rutas CLOUD (multi-tenant) =====
if IngestPayload and is_valid and set_snapshot and get_snapshot:
    @app.post("/api/ingest")
    def ingest(p: "IngestPayload", x_api_key: str = Header(...)):  # <-- quita convert_underscores=False
        if not is_valid(p.company, x_api_key):
            raise HTTPException(status_code=401, detail="Invalid API key")
        set_snapshot(p.company, p.model_dump())
        return {"ok": True}

    @app.get("/api/live")
    def live(company: str):
        data = get_snapshot(company)
        if not data:
            raise HTTPException(status_code=404, detail="No live data")
        return data

# ===== Rutas LOCALES (stubs) =====
@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "OK", "detail": "API alive"}

@app.get("/tags")
def tags_stub():
    return {"HR1": 123, "HR2": 456}

@app.get("/io")
def io_stub():
    return {"Y0": 1, "Y1": 0, "Y2": 0}

# ===== Frontend: / redirige a /web =====
@app.get("/")
def root():
    return RedirectResponse(url="/web/")

# Monta estáticos sin pisar rutas API
app.mount("/web", StaticFiles(directory="web", html=True), name="web")
