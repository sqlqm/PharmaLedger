import argparse
import logging
from pathlib import Path
import sys

import json
import pandas as pd
from chain import Chain


def load_units_csv(path: str = "dscsa_transactions_2024_2025.csv") -> pd.DataFrame:
    """Load the units CSV and perform light validation.

    - Ensures the file exists.
    - Reads all columns as strings and avoids pandas' default NA conversions
      which can turn some string-looking values into NaN.
    - Strips whitespace from column names and checks required columns exist.

    Returns a DataFrame with empty strings for missing cells.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV file not found: {p.resolve()}")

    # read as strings and avoid converting default NA tokens
    df = pd.read_csv(p, dtype=str, keep_default_na=False).fillna("")
    # normalize column names (strip accidental whitespace)
    df.columns = df.columns.str.strip()

    # basic sanity checks (fail fast if the file is wrong)
    required = {"barcode_string", "gtin", "serial", "exp", "lot", "status"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{p.name} is missing required columns: {sorted(missing)}")

    return df


def main(argv=None):
    parser = argparse.ArgumentParser(description="Load and inspect units CSV file")
    parser.add_argument("--path", "-p", default="dscsa_transactions_2024_2025.csv", help="Path to units CSV file")
    parser.add_argument("--build-chain", action="store_true", help="Build a Chain from the CSV rows")
    parser.add_argument("--chain-output", default=None, help="If set, write the built chain to this JSON file")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    try:
        units = load_units_csv(args.path)
    except Exception as e:
        logging.error("Failed to load CSV: %s", e)
        sys.exit(2)

    logging.info("Loaded %d rows from %s", len(units), args.path)
    # show first rows (ensure we don't trigger scientific-formatting by casting to string)
    logging.info("\n%s", units.head(5).to_string(index=False))

    # integrity check
    cols = ["barcode_string", "gtin", "serial", "lot", "exp", "status"]
    missing_counts = units[cols].eq("").sum()
    logging.info("\nMissing values per column:")
    logging.info("%s", missing_counts)

    # print all 2D barcodes only
    logging.info("\nAll 2D Barcodes:")
    for i, code in enumerate(units["barcode_string"], start=1):
        logging.info(f"{i:02d}. {code}")
    # optionally build a Chain from CSV rows
    if args.build_chain:
        logging.info("\nBuilding Chain from CSV rows...")
        chain = Chain(genesis_data={"source": Path(args.path).name, "rows": len(units)})

        # choose which columns to include in each block's data
        block_cols = ["barcode_string", "gtin", "serial", "lot", "exp", "status"]
        for _, row in units.iterrows():
            # create a plain dict for the block payload
            payload = {c: row.get(c, "") for c in block_cols}
            chain.add_block(payload)

        logging.info("Chain built: %d blocks", len(chain))

        if args.chain_output:
            out = Path(args.chain_output)
            try:
                with out.open("w", encoding="utf-8") as fh:
                    json.dump(chain.to_list(), fh, indent=2, ensure_ascii=False)
                logging.info("Wrote chain JSON to %s", out)
            except Exception as e:
                logging.error("Failed to write chain JSON: %s", e)


if __name__ == "__main__":
    main()