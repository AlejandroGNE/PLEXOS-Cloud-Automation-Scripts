# Run a PLEXOS model locally

This script uses `PLEXOS64.exe` directly. It does not import the older Python PLEXOS API or modify model inputs. It writes an engine console log, checks that a solution ZIP exists, and optionally uses the PLEXOS Cloud CLI to convert the ZIP to Parquet. The output path sent to `PLEXOS64.exe` is absolute to avoid ambiguity about where a relative `\o` path will land.

```powershell
python run_local_model.py `
  --xml 'C:\models\Study\database.xml' `
  --model 'Example Model' `
  --engine 'C:\Program Files\Energy Exemplar\PLEXOS 12.0\PLEXOS64.exe' `
  --output-dir 'C:\work\example-run' `
  --cloud-cli "$env:LOCALAPPDATA\Programs\PLEXOS.Cloud\plexos-cloud.exe"
```

The XML must still have access to its referenced Data Files, CSVs, and other inputs in their original relative locations. Supply a **new** output directory for every run; an existing directory is rejected. Omit `--cloud-cli` if you only need the solution ZIP. The script writes `run.json` with the resolved paths. If a stage fails, inspect `engine-console.log`, the engine's model log under `solutions/`, or `conversion.log`.

The CLI install path above is an example; find `plexos-cloud.exe` on your computer rather than assuming that path. Local execution requires a compatible PLEXOS installation and license. Cloud pre/post-simulation scripts use a different file layout and environment variables; see the root repository README for that workflow.
