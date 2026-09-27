"""Summarize marked fallback usage in exported rain-cell GeoJSON files."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def summarize_file(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as stream:
        features = json.load(stream).get("features", [])

    track_ids = {
        str(feature.get("properties", {}).get("trackId"))
        for feature in features
        if feature.get("properties", {}).get("trackId") is not None
    }
    fallback_ids = {
        str(feature.get("properties", {}).get("trackId"))
        for feature in features
        if feature.get("properties", {}).get("fallback_used", False)
    }
    total = len(track_ids)
    fallback = len(fallback_ids)
    return {
        "file": path.name,
        "feature_count": len(features),
        "unique_track_count": total,
        "fallback_track_count": fallback,
        "fallback_track_rate": fallback / total if total else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    rows = [summarize_file(path) for path in sorted(args.input_dir.glob("*.json"))]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "file",
        "feature_count",
        "unique_track_count",
        "fallback_track_count",
        "fallback_track_rate",
    ]
    with args.output_csv.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
