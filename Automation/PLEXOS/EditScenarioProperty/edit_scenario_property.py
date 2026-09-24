"""Add one scenario-tagged property to a working copy of an existing XML model."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path

from plexos_sdk import Class, Collection, Object, PLEXOSSDK, Property, XmlConverter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-xml", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--model", required=True, help="Model that should use the scenario")
    parser.add_argument("--parent-class", required=True, help="Parent class of the target collection")
    parser.add_argument("--parent", required=True, help="Parent object name")
    parser.add_argument("--collection", required=True, help="Collection name on the parent class")
    parser.add_argument("--child", required=True, help="Child object name")
    parser.add_argument("--property", required=True, help="Property name on that collection")
    parser.add_argument("--scenario", required=True, help="Existing or new Scenario object name")
    parser.add_argument("--value", required=True, type=float)
    parser.add_argument("--date-from", help="Optional ISO date, e.g. 2030-01-01T00:00:00")
    return parser.parse_args()


def find_target(sdk: PLEXOSSDK, args: argparse.Namespace):
    parent_class = Class.get(Class.name == args.parent_class)
    collection = Collection.get(
        (Collection.parent_class_id == parent_class.class_id)
        & (Collection.name == args.collection)
    )
    property_obj = Property.get(
        (Property.collection_id == collection.collection_id)
        & (Property.name == args.property)
    )
    membership = sdk.get_membership_by_names(
        parent_class.lang_id, collection.lang_id, args.parent, args.child
    )
    return membership, property_obj


def scenario_records(sdk: PLEXOSSDK, membership, property_obj, scenario_name: str):
    return [
        row for row in sdk.get_property_data_all(membership, property_obj)
        if any(tag.object.name == scenario_name for tag in row.tags)
    ]


def edit(sdk: PLEXOSSDK, args: argparse.Namespace) -> None:
    model_class = Class.get(Class.name == "Model")
    scenario_class = Class.get(Class.name == "Scenario")
    model = sdk.get_object_by_name(model_class.lang_id, args.model)
    scenarios_collection = Collection.get(
        (Collection.parent_class_id == model_class.class_id)
        & (Collection.name == "Scenarios")
    )
    membership, property_obj = find_target(sdk, args)
    scenario = Object.select().where(
        (Object.class_id == scenario_class.class_id) & (Object.name == args.scenario)
    ).first()
    if scenario is not None and scenario_records(sdk, membership, property_obj, scenario.name):
        raise ValueError("This membership/property already has data tagged with that scenario")

    with sdk.transaction():
        if scenario is None:
            scenario = sdk.add_object(scenario_class.lang_id, args.scenario)
        attached = {
            item.child_object.name
            for item in sdk.get_child_memberships(
                model_class.lang_id, scenarios_collection.lang_id, model.name
            )
        }
        if scenario.name not in attached:
            sdk.add_membership(scenarios_collection, model, scenario)
        sdk.add_property(
            membership, property_obj, args.value,
            scenario_tag=scenario, date_from=args.date_from,
        )


def verify(export_xml: Path, check_db: Path, args: argparse.Namespace) -> None:
    with PLEXOSSDK.from_xml(export_xml, check_db) as sdk:
        membership, property_obj = find_target(sdk, args)
        matches = scenario_records(sdk, membership, property_obj, args.scenario)
        if len(matches) != 1 or matches[0].value != args.value:
            raise AssertionError("Tagged property value did not survive XML round-trip")
        if args.date_from and args.date_from not in {item.date for item in matches[0].date_from}:
            raise AssertionError("Start date did not survive XML round-trip")
        model_class = Class.get(Class.name == "Model")
        scenarios_collection = Collection.get(
            (Collection.parent_class_id == model_class.class_id)
            & (Collection.name == "Scenarios")
        )
        names = {
            item.child_object.name
            for item in sdk.get_child_memberships(
                model_class.lang_id, scenarios_collection.lang_id, args.model
            )
        }
        if args.scenario not in names:
            raise AssertionError("Model Scenario membership did not survive XML round-trip")


def main() -> None:
    args = parse_args()
    source = args.source_xml.resolve()
    destination = args.output_dir.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if destination.exists():
        raise FileExistsError(f"Choose a new output directory: {destination}")
    if destination.is_relative_to(source.parent):
        raise ValueError("Output directory must be outside the source XML directory")
    # Preserve the XML's relative references to CSVs, TimeSeries, and other files.
    shutil.copytree(source.parent, destination)
    copied_xml = destination / source.name
    exported_xml = destination / f"edited-{source.name}"
    with tempfile.TemporaryDirectory(prefix="plexos-sdk-roundtrip-") as scratch:
        scratch_path = Path(scratch)
        with PLEXOSSDK.from_xml(copied_xml, scratch_path / "working.db") as sdk:
            edit(sdk, args)
        XmlConverter().db_to_xml(str(scratch_path / "working.db"), str(exported_xml))
        verify(exported_xml, scratch_path / "verification.db", args)
    print(f"Verified edited XML: {exported_xml}")


if __name__ == "__main__":
    main()
