# Model-specific use cases

This directory is for **verified knowledge about particular PLEXOS projects**. The general SDK and solution-query documentation elsewhere in the repository applies across models; a use-case skill may describe the meaning of objects, scenarios, constraints, and reported series only for its identified source model.

Create `UseCases/<project-slug>/SKILL.md` from [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md). Include the source model/version, what was inspected, the exact evidence for each interpretation, validation results, and unresolved questions. A later session can refer to the repository and the relevant use-case skill directly; merely placing a skill here does not install it automatically into Codex.

## Public material boundary

Publish scripts, synthetic examples, and reviewed model notes. Do **not** commit model XML, input data, solution files, credentials, local paths containing private information, or generated databases by default. Add a toy XML only when its publication is explicitly approved and its inputs are synthetic or otherwise publishable. A use-case skill can cite a private model version or hash without including the model itself.

Keep claims tied to a model snapshot. When the model changes, recheck the relationships and solution metrics before carrying a conclusion forward.
