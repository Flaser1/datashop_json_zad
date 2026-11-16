

import json
from pathlib import Path


def read_orders(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if not isinstance(payload, dict):
        raise ValueError("JSON root must be an object")
    if payload.get("currency") != "PLN":
        raise ValueError("Expected currency PLN")
    if "orders" not in payload or not isinstance(payload["orders"], list):
        raise ValueError("orders must be a list")

    for record_number, row in enumerate(payload["orders"], start=1):
        if not isinstance(row, dict):
            raise ValueError(f"Order at record {record_number} must be an object")

    return payload["orders"]