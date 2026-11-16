

from pathlib import Path
from dataclasses import dataclass
from dotenv import dotenv_values

@dataclass(frozen=True)
class PipelineConfig:
    input_path: Path
    output_dir: Path

def load_config(dataset: str):
    base_dir = Path(__file__).resolve().parent
    env_path = base_dir / ".env"

    with env_path.open("r", encoding="utf-8") as file:
        properties = dotenv_values(stream=file, interpolate=False)

    input_path = properties.get(f"INPUT_PATH_{dataset}")
    output_dir = properties.get(f"OUTPUT_DIR_{dataset}")
    if input_path is None or not input_path.strip():
        raise ValueError(f"Set INPUT_PATH_{dataset} in .env")
    if output_dir is None or not output_dir.strip():
        raise ValueError(f"Set OUTPUT_DIR_{dataset} in .env")

    return PipelineConfig(
        base_dir / input_path,
        base_dir / output_dir,
    )
