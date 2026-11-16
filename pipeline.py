

from pathlib import Path
from ingestion import read_orders
from transformations import transform_orders
from exporting import export_orders


def run_pipeline(input_path: Path, output_dir: Path) -> dict:
    raw_orders = read_orders(input_path)
    clean, rejected = transform_orders(raw_orders, input_path.name)
    export_orders(output_dir, clean, rejected)

    return {
        "source_file": input_path.name,
        "input_rows_count": len(raw_orders),
        "clean": clean,
        "rejected": rejected,
    }