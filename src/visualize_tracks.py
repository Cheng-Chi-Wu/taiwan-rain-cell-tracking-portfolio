"""Render exported rain-cell GeoJSON tracks and build an optional GIF.

This script consumes outputs from the tracking system; it does not reproduce
or redistribute the upstream tracking engine.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from shapely.geometry import Polygon


def read_features(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as stream:
        document = json.load(stream)
    return document.get("features", [])


def color_for_track(track_id: str, color_index: dict[str, int]):
    if track_id not in color_index:
        color_index[track_id] = len(color_index)
    return plt.get_cmap("tab20")(color_index[track_id] % 20)


def render_frame(
    track_file: Path,
    boundary: gpd.GeoDataFrame,
    output_path: Path,
    color_index: dict[str, int],
    bounds: tuple[float, float, float, float] | None = None,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 7))
    boundary.plot(ax=ax, color="white", edgecolor="black", linewidth=0.6)

    for feature in read_features(track_file):
        properties = feature.get("properties", {})
        coordinates = feature.get("geometry", {}).get("coordinates", [])
        if not coordinates:
            continue
        polygon = Polygon(np.asarray(coordinates[0]))
        track_id = str(properties.get("trackId", "unknown"))
        color = color_for_track(track_id, color_index)
        x_coord, y_coord = polygon.exterior.xy
        ax.fill(x_coord, y_coord, color=color, alpha=0.75)
        centroid = polygon.centroid
        marker = "x" if properties.get("fallback_used", False) else "o"
        ax.plot(centroid.x, centroid.y, marker=marker, color="black", ms=4)

    if bounds:
        west, east, south, north = bounds
        ax.set_xlim(west, east)
        ax.set_ylim(south, north)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(track_file.stem)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.25)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def create_gif(frames: list[Path], output_path: Path, duration_ms: int) -> None:
    if not frames:
        raise ValueError("No rendered frames were available for the GIF.")
    images = [Image.open(path).convert("RGB") for path in frames]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration_ms,
        loop=0,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tracks_dir", type=Path)
    parser.add_argument("boundary_file", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--gif", type=Path)
    parser.add_argument("--duration-ms", type=int, default=500)
    parser.add_argument("--bounds", nargs=4, type=float, metavar=("W", "E", "S", "N"))
    args = parser.parse_args()

    boundary = gpd.read_file(args.boundary_file)
    color_index: dict[str, int] = {}
    rendered: list[Path] = []
    for track_file in sorted(args.tracks_dir.glob("*.json")):
        output_path = args.output_dir / f"{track_file.stem}.png"
        render_frame(track_file, boundary, output_path, color_index, args.bounds)
        rendered.append(output_path)

    if args.gif:
        create_gif(rendered, args.gif, args.duration_ms)
    print(f"Rendered {len(rendered)} track frames.")


if __name__ == "__main__":
    main()

