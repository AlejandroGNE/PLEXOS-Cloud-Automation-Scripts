"""List classes, properties, units, and period types reported in a Parquet solution."""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parquet-dir", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    args = parser.parse_args()
    parquet = args.parquet_dir.resolve()
    output = args.output_csv.resolve()
    if not any((parquet / "fullkeyinfo").rglob("*.parquet")):
        raise FileNotFoundError(f"No fullkeyinfo Parquet files under {parquet}")
    if output.exists():
        raise FileExistsError(f"Choose a new CSV path: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    fullkeyinfo = (parquet / "fullkeyinfo" / "**" / "*.parquet").as_posix()
    # The metadata table describes the reported series without assuming what
    # any particular class/property means in the input model.
    with duckdb.connect() as con:
        rows = con.execute("""
            SELECT ChildClassName, PropertyName, UnitValue, PeriodTypeName,
                   COUNT(*) AS SeriesCount
            FROM read_parquet(?)
            GROUP BY 1, 2, 3, 4
            ORDER BY 1, 2, 3, 4
        """, [fullkeyinfo]).fetchall()
    import csv

    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["ChildClassName", "PropertyName", "UnitValue", "PeriodTypeName", "SeriesCount"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} reported series combinations: {output}")


if __name__ == "__main__":
    main()
