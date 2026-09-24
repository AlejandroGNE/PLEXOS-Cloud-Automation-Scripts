# Query a PLEXOS solution in Parquet

PLEXOS Cloud post-simulation tasks can create DuckDB views over solution Parquet using [ConfigureDuckDbViews](../Post/PLEXOS/ConfigureDuckDbViews/). For a ZIP produced by a local `PLEXOS64.exe` run, first use `plexos-cloud solution convert zip-to-parquet --zipPath <zip> --outputDirectory <directory>`. The [LocalRun](../Automation/PLEXOS/LocalRun/) example can do both steps.

## Discover before calculating

Start with the [SolutionSeriesCatalog](../Automation/PLEXOS/SolutionSeriesCatalog/) or inspect `fullkeyinfo` directly:

```sql
SELECT DISTINCT ChildClassName, PropertyName, UnitValue, PeriodTypeName
FROM read_parquet('<solution>/fullkeyinfo/**/*.parquet')
ORDER BY 1, 2, 3, 4;
```

Output property names can look similar while representing different quantities. A policy or engineering metric should be mapped from the **input model's equation and participating objects** to a reported output series. Do not infer this mapping solely from class names, fuel categories, or a familiar output label.

## Join values to series and periods

The observed local conversion layout has `fullkeyinfo`, `data`, and `period` subdirectories. `SeriesId` joins the series metadata to values; `PeriodId` joins values to calendar periods:

```sql
SELECT f.ChildClassName, f.ChildObjectName, f.PropertyName,
       f.UnitValue, f.PeriodTypeName, p.StartDate, d.Value
FROM read_parquet('<solution>/fullkeyinfo/**/*.parquet') AS f
JOIN read_parquet('<solution>/data/**/*.parquet') AS d
  ON f.SeriesId = d.SeriesId
JOIN read_parquet('<solution>/period/**/*.parquet') AS p
  ON d.PeriodId = p.PeriodId
WHERE f.ChildClassName = ?
  AND f.PropertyName = ?
  AND f.PeriodTypeName = 'Year'
  AND EXTRACT(YEAR FROM p.StartDate) = ?;
```

Use query parameters for class, property, and year. Check `UnitValue` **before** summing or comparing values; an annual energy series and an interval power series are not interchangeable. Verify the expected number of objects and periods. A configured report may omit inactive objects or properties that were never requested. Missing series do not automatically mean zero.

For sampled simulations, prefer a reported annual total when it represents the desired measure. If rebuilding annual values from sampled intervals, inspect the solution's sample weights and PLEXOS aggregation rules instead of summing the sampled intervals as if they were a full year.
