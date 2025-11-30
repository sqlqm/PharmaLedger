import argparse
import json
from pathlib import Path

import pandas as pd

from chain import Chain


def load_units_csv(path="dscsa_transactions_2024_2025.csv"):
    file_path = Path(path)

    # Check that the file actually exists
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path.resolve()}")

    # Read the CSV file. We specify dtype=str so everything is read as text.
    # keep_default_na=False and fillna("") so we don't get NaN values.
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False).fillna("")

    # Remove leading/trailing spaces from column names, just in case
    df.columns = df.columns.str.strip()

    # These are the columns our script expects to exist
    required_columns = ["barcode_string", "gtin", "serial", "exp", "lot", "status"]

    # Check if any required column is missing
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            f"{file_path.name} is missing required columns: {missing}"
        )

    return df


def main():
    # Simple command-line argument setup
    parser = argparse.ArgumentParser(
        description="Load DSCSA units CSV and optionally build a blockchain."
    )

    parser.add_argument(
        "--path",
        "-p",
        default="dscsa_transactions_2024_2025.csv",
        help="Path to the units CSV file",
    )

    parser.add_argument(
        "--build-chain",
        action="store_true",
        help="If set, build a Chain from the CSV rows",
    )

    parser.add_argument(
        "--chain-output",
        default=None,
        help="If set, write the built chain to this JSON file",
    )

    args = parser.parse_args()

    # Try to load the CSV
    try:
        units = load_units_csv(args.path)
    except Exception as e:
        print("Error: could not load CSV file.")
        print("Details:", e)
        return

    # Basic information about the data
    print(f"Loaded {len(units)} rows from {args.path}")

    print("\nFirst 5 rows:")
    # Use to_string(index=False) so we don't show the pandas index column
    print(units.head(5).to_string(index=False))

    # Columns we care about for simple checks
    columns_to_check = ["barcode_string", "gtin", "serial", "lot", "exp", "status"]

    print("\nMissing values per column:")
    for col in columns_to_check:
        # Count how many rows have an empty string in this column
        missing_count = (units[col] == "").sum()
        print(f"{col}: {missing_count}")

    # Print all barcode_string values
    print("\nAll 2D Barcodes:")
    for i, code in enumerate(units["barcode_string"], start=1):
        print(f"{i:02d}. {code}")

    # If the user asked to build the chain
    if args.build_chain:
        print("\nBuilding Chain from CSV rows...")

        # The genesis block will store basic info about the source
        genesis_data = {
            "source": Path(args.path).name,
            "rows": len(units),
        }

        chain = Chain(genesis_data=genesis_data)

        # These are the columns we put inside each block's data
        block_columns = ["barcode_string", "gtin", "serial", "lot", "exp", "status"]

        # Loop over each row in the DataFrame and add a block
        for _, row in units.iterrows():
            # Turn the row into a simple dictionary
            payload = {}
            for col in block_columns:
                # row[col] is a pandas Series, but we just want the value
                payload[col] = row.get(col, "")

            chain.add_block(payload)

        print(f"Chain built: {len(chain)} blocks")

        # If the user also asked to save the chain to a file
        if args.chain_output:
            output_path = args.chain_output
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(chain.to_list(), f, indent=2, ensure_ascii=False)
                print(f"Wrote chain JSON to {output_path}")
            except Exception as e:
                print("Error: could not write chain JSON.")
                print("Details:", e)


if __name__ == "__main__":
    main()