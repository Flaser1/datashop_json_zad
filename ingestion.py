

import json
from pathlib import Path


def read_orders(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    return payload["orders"]