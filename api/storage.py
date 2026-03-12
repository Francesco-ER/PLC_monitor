# api/storage.py
import json, os, time
from typing import Any, Optional

_mem = {}  # Fallback en memoria para DEV

# Intentar Redis; si falla, usamos _mem
_r = None
try:
    from redis import Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    _r = Redis.from_url(REDIS_URL, decode_responses=True)
    _r.ping()  # verifica conexión
except Exception:
    _r = None

def set_snapshot(company: str, payload: dict, ttl: int = 15) -> None:
    data = {**payload, "_ts": time.time()}
    if _r:
        _r.set(f"live:{company}", json.dumps(data), ex=ttl)
    else:
        _mem[f"live:{company}"] = (data, time.time() + ttl)

def get_snapshot(company: str) -> Optional[dict[str, Any]]:
    if _r:
        raw = _r.get(f"live:{company}")
        return json.loads(raw) if raw else None
    item = _mem.get(f"live:{company}")
    if not item:
        return None
    data, expires = item
    if time.time() > expires:
        _mem.pop(f"live:{company}", None)
        return None
    return data
