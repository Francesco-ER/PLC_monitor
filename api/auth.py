import json
import os
from functools import lru_cache


TENANTS_PATH = os.getenv("TENANTS_PATH", os.path.join(os.path.dirname(__file__), "tenants.json"))


@lru_cache(maxsize=1)
def _load_tenants():
  with open(TENANTS_PATH, "r", encoding="utf-8") as f:
    return json.load(f)


def is_valid(company: str, api_key: str) -> bool:
  t = _load_tenants().get(company)
  return bool(t and t.get("api_key") == api_key)


def get_companies() -> list[str]:
  return list(_load_tenants().keys())