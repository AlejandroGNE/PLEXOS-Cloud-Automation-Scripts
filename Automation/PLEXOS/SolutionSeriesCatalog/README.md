# Discover the series in a Parquet solution

Run this after converting a solution ZIP to Parquet (or against an existing Parquet solution directory):

```powershell
python catalog_solution_series.py `
  --parquet-dir 'C:\work\example-run\parquet' `
  --output-csv 'C:\work\example-run\series-catalog.csv'
```

The catalog lists every reported combination of `ChildClassName`, `PropertyName`, `UnitValue`, and `PeriodTypeName`. It helps you choose a query based on what the solution actually contains. It **does not** determine which series implements a policy or business metric; inspect the input model's objects, constraint memberships, property data, and tags for that.

For a targeted annual result query, see [Solution Parquet query cookbook](../../../Documentation/Solution_Parquet_Query_Cookbook.md). This script requires DuckDB and rejects an existing output CSV.
