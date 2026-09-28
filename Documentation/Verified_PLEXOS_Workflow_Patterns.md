# Verified PLEXOS workflow patterns

These checks came from a local PLEXOS automation pilot. They describe reusable ways to edit a model, run it, and interpret a solution. Object names, model equations, and the meaning of a particular scenario must still be established from each study. The observed failures are examples, not claims that every PLEXOS version behaves the same way.

## Edit model inputs through the installed SDK

1. Identify the installed `plexos_sdk` wheel and inspect the signatures and model fields used by the script. The repository examples may target a newer wheel; see [SDK version compatibility](SDK_Version_Compatibility.md).
2. Import the source XML into a disposable database. Keep the source XML and its hash. Query the actual classes, collections, properties, memberships, and scenario tags before editing. Do not assume a collection's cardinality or that a new object needs a manually added System membership: `add_object` can create that membership automatically.
3. Try a small SDK transaction, export XML, reimport it, and check the resulting objects, memberships, property values, tags, and model-to-scenario links. Preserve earlier scenario versions when a study relies on them.
4. For a repeated SDK operation, benchmark several increasing, realistic batch sizes. A successful three-row round trip says little about the cost of thousands of `add_property` calls. Record row counts, elapsed times, wheel version, and machine context before choosing a full-scale approach.
5. Report an SDK limitation with a minimal reproducible example, expected and actual behavior, version, and round-trip result. If a project owner authorizes a direct-database exception, isolate it to the named model and operation, validate the exported XML, and record when the exception should be removed. An exception is not a general recommendation for direct SQL input edits.

## Run a disposable model copy

Some local engine runs may upgrade an XML in place. Copy the XML and referenced inputs into a run directory, record the source hash, and point `PLEXOS64.exe` at the copy. Record the engine version, model, scenarios, horizon, and result location. A one-day smoke test is useful, but it cannot establish full-year behavior or output coverage.

Before changing horizon counts, determine what each count means in that model: chronological steps, planning steps, and look-ahead can have different units. Check the solved period metadata **and** the timestamps and values of the required output series after the run.

## Validate solution series before calculating a metric

Use the [Parquet query cookbook](Solution_Parquet_Query_Cookbook.md) to discover series metadata. For each required series, state its class, object, property, phase, period type, sample, and unit. Then check:

- expected object and interval counts; distinct, contiguous timestamps; and missing or duplicate values;
- the period duration and any sample weights before converting MW to MWh or calculating annual totals;
- whether a missing reported series means an inactive object, an unrequested report, or an actual zero;
- whether the chosen output measures the physical quantity or a broader accounting quantity.

In the pilot, a solution period table listed 8,760 hours while required value series contained 8,712 values. The final 48 hours were absent because of the configured horizon and look-ahead. A count of period rows alone would have missed the incomplete output. In another check, Market-cleared quantities included activity beyond physical Battery dispatch. Comparing object-level Battery Load/Generation with Market Purchases/Sales and the regional balance exposed the distinction. These are study-specific observations; inspect the equations and series in a new model before reusing the mapping.

## Compare scenarios and aggregate by location

Resolve each simulation ID to its model, scenarios, source version, solution ID, and run settings before comparing outputs. Fix random seeds where possible and flag comparisons made with different seeds. Reconcile interval totals to annual summaries and use identities appropriate to the modeled objects; do not treat a completed solve as proof that runs are comparable.

Check relationship multiplicity before joining an object series to Regions, Zones, or Nodes. An object can have multiple relevant memberships, so a plain join can duplicate its output. Define the intended mapping or allocation rule, then verify that system totals reconcile to the regional totals. A pilot regional renewable query double-counted generators with two Region memberships.

For large Cloud solutions, write a small manifest of simulation ID, model, solution ID, expected files, and file sizes. Downloads can leave incomplete or zero-byte files while running. Verify existing files before re-downloading, keep raw solutions outside Git, and preserve only the retrieval recipe and reviewed results. Before declaring a report complete, inventory historical figures and their source queries; validate every recovered plot against the current solution schema and study meaning.
