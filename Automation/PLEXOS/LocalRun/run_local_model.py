"""Run one PLEXOS Model from XML locally and optionally convert its ZIP to Parquet."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xml", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--engine", required=True, type=Path, help="Full path to PLEXOS64.exe")
    parser.add_argument("--output-dir", required=True, type=Path, help="New directory for logs and solution")
    parser.add_argument("--cloud-cli", type=Path, help="Full path to plexos-cloud executable; enables Parquet conversion")
    args = parser.parse_args()

    xml = args.xml.resolve()
    engine = args.engine.resolve()
    output = args.output_dir.resolve()
    if not xml.is_file() or not engine.is_file():
        raise FileNotFoundError("XML model or PLEXOS64.exe not found")
    if args.cloud_cli and not args.cloud_cli.resolve().is_file():
        raise FileNotFoundError(args.cloud_cli)
    if output.exists():
        raise FileExistsError(f"Choose a new output directory: {output}")
    output.mkdir(parents=True)

    solution_dir = output / "solutions"
    solution_dir.mkdir()
    command = [str(engine), str(xml), r"\n", r"\o", str(solution_dir), r"\m", args.model]
    with (output / "engine-console.log").open("w", encoding="utf-8") as log:
        subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)

    zip_path = solution_dir / f"Model {args.model} Solution" / f"Model {args.model} Solution.zip"
    if not zip_path.is_file():
        raise FileNotFoundError(f"Engine exited successfully but the expected solution ZIP is missing: {zip_path}")

    manifest = {"model": args.model, "xml": str(xml), "engine": str(engine), "solution_zip": str(zip_path)}
    if args.cloud_cli:
        parquet = output / "parquet"
        with (output / "conversion.log").open("w", encoding="utf-8") as log:
            subprocess.run(
                [str(args.cloud_cli.resolve()), "solution", "convert", "zip-to-parquet",
                 "--zipPath", str(zip_path), "--outputDirectory", str(parquet)],
                stdout=log, stderr=subprocess.STDOUT, check=True,
            )
        for required in ("fullkeyinfo", "data", "period"):
            if not any((parquet / required).rglob("*.parquet")):
                raise FileNotFoundError(f"Parquet conversion lacks {required}: {parquet}")
        manifest["parquet"] = str(parquet)
    (output / "run.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
