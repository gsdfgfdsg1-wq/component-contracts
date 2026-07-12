#!/usr/bin/env python3
"""Compare component API snapshots and classify compatibility changes."""
import argparse
import json
from pathlib import Path


def compare(before, after):
    changes = []
    for component, old_api in before.items():
        if component not in after:
            changes.append({"component": component, "kind": "component-removed", "level": "major"})
            continue
        new_api = after[component]
        old_props, new_props = old_api.get("props", {}), new_api.get("props", {})
        for prop in old_props:
            if prop not in new_props:
                changes.append({"component": component, "kind": "prop-removed", "prop": prop, "level": "major"})
            elif set(new_props[prop].get("values", [])) - set(old_props[prop].get("values", [])):
                pass
            elif set(old_props[prop].get("values", [])) - set(new_props[prop].get("values", [])):
                changes.append({"component": component, "kind": "enum-narrowed", "prop": prop, "level": "major"})
            elif old_props[prop].get("default") != new_props[prop].get("default"):
                changes.append({"component": component, "kind": "default-changed", "prop": prop, "level": "minor"})
        for prop, definition in new_props.items():
            if prop not in old_props and definition.get("required"):
                changes.append({"component": component, "kind": "required-prop-added", "prop": prop, "level": "major"})
    level = "major" if any(c["level"] == "major" for c in changes) else "minor" if changes else "patch"
    return {"recommended_bump": level, "changes": changes, "compatible": level != "major"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before"); parser.add_argument("after")
    args = parser.parse_args()
    report = compare(json.loads(Path(args.before).read_text()), json.loads(Path(args.after).read_text()))
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["compatible"] else 1)


if __name__ == "__main__":
    main()
