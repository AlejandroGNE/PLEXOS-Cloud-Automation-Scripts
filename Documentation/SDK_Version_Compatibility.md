# Match SDK examples to the installed wheel

The repository's `PLEXOS_SDK_TLDR.md` is labelled **SDK 1.0.179+**. A local PLEXOS Cloud CLI can ship an older SDK wheel. Consult the documentation bundled with the **installed CLI** and check your Python environment before copying a call from this repository. The Cloud SDK (`eecloud`) and input-editing PLEXOS SDK (`plexos_sdk`) are different packages.

## Check the environment

```powershell
python -c "from importlib.metadata import version; from plexos_sdk import PLEXOSSDK; print('plexos_sdk', version('plexos_sdk')); print('copy_object available:', hasattr(PLEXOSSDK, 'copy_object'))"
```

Use the `python` executable that will run your script, such as the Python in its virtual environment. On Windows, locate the Cloud CLI installation and inspect its adjacent wheel and `Documentation` directory. Do not assume a fixed installation directory name.

## Observed version difference

With the CLI-bundled **plexos_sdk 1.0.146.7**, `PLEXOSSDK.copy_object` was absent. The repository's 1.0.179+ quick reference documents it. A tagged `Tag` object inspected in 1.0.146.7 exposed `tag.object`, while the 1.0.179+ quick reference shows `tag.object_ref`. This is a version difference, not evidence that either documented release is defective.

For older wheels, use supported SDK methods to create objects, memberships, properties, and attributes; verify all required attributes rather than treating copied memberships as a complete clone. Inspect a real object's fields or the installed `PLEXOS_SDK_Methods.md` before following a version-specific relationship example. For a method you expect to exist, confirm its signature with `inspect.signature` before building a large workflow.

When reporting a possible SDK issue, include the wheel version, CLI version, a minimal input model if publishable, the exact call, expected and actual result, and whether an XML export/reimport preserves the change. Do not use direct SQL writes to hide an input-editing SDK failure.
