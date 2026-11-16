

from config import load_config
from pipeline import run_pipeline
from reporting import print_summary

def main() -> None:
    raw_orders = load_config("ORDERS")
    result = run_pipeline(raw_orders.input_path, raw_orders.output_dir)
    print_summary(result)

if __name__ == "__main__":
    main()