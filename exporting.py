

import json
from pathlib import Path

def write_json(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2, allow_nan=False)

def export_orders(output_dir: Path, clean: list[dict], rejected: list[dict]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    clean_rows = []
    for order in clean:
        row = order.copy()
        row["amount"] = str(order["amount"])
        clean_rows.append(row)

    write_json(output_dir / "clean_orders.json", clean_rows)
    write_json(output_dir / "rejected_orders.json", rejected)

