# Edit one scenario-tagged property in an existing XML

This local example uses the input-editing `plexos_sdk`. It copies the directory containing the source XML and its relative input files, adds one tagged property value, attaches the Scenario to one Model, exports a new XML, and reimports it to verify the value, tag, date, and Model membership. It does not modify the source directory or use direct SQL writes.

Install the PLEXOS SDK wheel bundled with your PLEXOS Cloud CLI. The version of the wheel determines the supported SDK calls; see [SDK version compatibility](../../../Documentation/SDK_Version_Compatibility.md).

```powershell
python edit_scenario_property.py `
  --source-xml 'C:\models\Study\database.xml' `
  --output-dir 'C:\work\Study-edited' `
  --model 'Example Model' `
  --parent-class 'Generator' --parent 'Example Generator' `
  --collection 'Constraints' --child 'Example Constraint' `
  --property 'Generation Coefficient' `
  --scenario 'Example Sensitivity' --value 1 `
  --date-from '2030-01-01T00:00:00'
```

The object and property names above are **illustrative**. Inspect the actual model before choosing them. A property belongs to a particular parent-class collection; matching only its name is insufficient. The script rejects an existing scenario-tagged record on the same membership/property to avoid silently stacking overrides. It requires a new output directory outside the source XML directory and retains the copy for inspection if a step fails. The verified result is `edited-<source XML name>` in that output directory.

This example verifies that an SDK edit survives an XML round-trip. It does not prove the new scenario has the intended modeling effect; run and inspect a solution for that.
