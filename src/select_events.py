"""Select sustained high-reflectivity events from radar HDF5 files.

Portfolio refactoring of event-screening code written during the NTU
rain-cell research project. Raw research data is intentionally excluded.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import h5py
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class EventConfig:
    threshold_dbz: float = 35.0
    clip_dbz: float = 75.0
    minimum_duration_minutes: int = 60
    timestep_minutes: int = 10
    dataset_key: str = "dataset1/data1/data"


def timestamp_from_filename(path: Path, utc_offset_hours: int) -> datetime:
    """Parse MREF3D21L.YYYYMMDD.HHMM.hdf5 into local time."""
    parts = path.name.split(".")
    if len(parts) < 4:
        raise ValueError(f"Unexpected radar filename: {path.name}")
    timestamp = datetime.strptime(parts[-3] + parts[-2], "%Y%m%d%H%M")
    return timestamp + timedelta(hours=utc_offset_hours)


def load_max_reflectivity(path: Path, dataset_key: str) -> float:
    """Return the maximum finite reflectivity in one radar frame."""
    with h5py.File(path, "r") as radar_file:
        values = np.asarray(radar_file[dataset_key][:], dtype=float)
    return float(np.nanmax(values))


def scan_frames(
    radar_dir: Path,
    config: EventConfig,
    utc_offset_hours: int = 8,
) -> pd.DataFrame:
    """Build a timestamped table of maximum reflectivity per frame."""
    rows: list[dict[str, object]] = []
    for path in sorted(radar_dir.glob("MREF3D21L.*.hdf5")):
        try:
            rows.append(
                {
                    "time": timestamp_from_filename(path, utc_offset_hours),
                    "max_dbz": load_max_reflectivity(path, config.dataset_key),
                    "source_file": path.name,
                }
            )
        except (KeyError, OSError, ValueError):
            continue
    return pd.DataFrame(rows).sort_values("time").reset_index(drop=True)


def select_events(frames: pd.DataFrame, config: EventConfig) -> pd.DataFrame:
    """Return consecutive high-dBZ blocks meeting the duration threshold."""
    if frames.empty:
        return pd.DataFrame()

    work = frames.copy()
    work["high_dbz"] = work["max_dbz"] >= config.threshold_dbz
    expected_gap = timedelta(minutes=config.timestep_minutes)
    work["block"] = (
        work["high_dbz"].ne(work["high_dbz"].shift())
        | work["time"].diff().ne(expected_gap)
    ).cumsum()

    events: list[dict[str, object]] = []
    for _, group in work.loc[work["high_dbz"]].groupby("block"):
        duration = len(group) * config.timestep_minutes
        if duration < config.minimum_duration_minutes:
            continue
        unclipped = group["max_dbz"]
        quality_values = unclipped.loc[unclipped <= config.clip_dbz]
        events.append(
            {
                "start_time": group["time"].iloc[0],
                "end_time": group["time"].iloc[-1],
                "duration_minutes": duration,
                "frame_count": len(group),
                "mean_dbz_below_clip": quality_values.mean(),
                "maximum_dbz": unclipped.max(),
            }
        )
    return pd.DataFrame(events)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("radar_dir", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--threshold-dbz", type=float, default=35.0)
    parser.add_argument("--minimum-duration", type=int, default=60)
    parser.add_argument("--utc-offset", type=int, default=8)
    args = parser.parse_args()

    config = EventConfig(
        threshold_dbz=args.threshold_dbz,
        minimum_duration_minutes=args.minimum_duration,
    )
    frames = scan_frames(args.radar_dir, config, args.utc_offset)
    events = select_events(frames, config)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(args.output_csv, index=False)
    print(f"Selected {len(events)} events from {len(frames)} radar frames.")


if __name__ == "__main__":
    main()

