import os, time, json
from dotenv import load_dotenv
import requests
from pymodbus.client import ModbusTcpClient


load_dotenv()
PLC_IP = os.getenv("PLC_IP", "127.0.0.1")
PLC_PORT = int(os.getenv("PLC_PORT", "502"))
UNIT_ID = int(os.getenv("UNIT_ID", "1"))
COMPANY_CODE = os.getenv("COMPANY_CODE", "demo")
API_KEY = os.getenv("API_KEY", "DEMO-API-KEY")
INGEST_URL = os.getenv("INGEST_URL", "http://127.0.0.1:8080/api/ingest")
PERIOD_S = float(os.getenv("PERIOD_S", "1.0"))


# Ajusta estas bases según tu mapa real
Y_BASE = int(os.getenv("Y_BASE", "114")) # coil base para salidas Y
Y_COUNT = int(os.getenv("Y_COUNT", "8")) # cuántas Y leer
HR_BASE = int(os.getenv("HR_BASE", "1")) # holding registers base
HR_COUNT = int(os.getenv("HR_COUNT", "10"))


def read_snapshot(c: ModbusTcpClient) -> dict:
  values = {}
  coils = c.read_coils(Y_BASE, Y_COUNT, unit=UNIT_ID)
  if hasattr(coils, "isError") and not coils.isError():
    for i, v in enumerate(coils.bits[:Y_COUNT]):
      values[f"Y{i}"] = int(bool(v))
  hrs = c.read_holding_registers(HR_BASE, HR_COUNT, unit=UNIT_ID)
  if hasattr(hrs, "isError") and not hrs.isError():
    for i, v in enumerate(hrs.registers[:HR_COUNT]):
      values[f"HR{HR_BASE + i}"] = v
  return values



def loop():
  while True:
    try:
      with ModbusTcpClient(PLC_IP, port=PLC_PORT) as c:
        snapshot = read_snapshot(c)
      payload = {"company": COMPANY_CODE, "ts": time.time(), "values": snapshot}
      headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
      r = requests.post(INGEST_URL, headers={"X-API-Key": API_KEY}, json=payload, timeout=5)
      print("INGEST →", r.status_code, r.text)
    except Exception:
      # backoff simple ante cortes
      time.sleep(min(PERIOD_S * 2, 5))
    time.sleep(PERIOD_S)  



if __name__ == "__main__":
  loop()