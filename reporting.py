

def print_summary(result: dict) -> None:
    print(f"File: {result['source_file']}")
    print(f"Number of records: {result['input_rows_count']}")
    print(f"Number of clean records: {len(result["clean"])}")
    print(f"Number of rejected records: {len(result["rejected"])}")
    print(result["clean"])