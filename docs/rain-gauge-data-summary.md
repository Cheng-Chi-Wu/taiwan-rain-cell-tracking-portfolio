# Rain Gauge Dataset Summary

This summary describes the portion of the rain-gauge observations used during the research project. The statistics were calculated across 194 daily CSV files in the authorized local research directory.

## Coverage

- 194 CSV files, including 193 files with observations and one header-only file
- 191 MB of source data
- 2,803,229 observation rows
- 113 unique rain-gauge stations
- 27,192 unique observation timestamps
- Observation period from June 1, 2021 through September 7, 2023

## Rainfall field quality

The `RAIN` field uses negative sentinel values to represent unavailable observations.

- 535,405 valid nonnegative rainfall observations, or 19.10% of all rows
- 2,263,966 observations encoded as `-998`
- 3,858 observations encoded as `-999`
- 229,388 positive rainfall observations
- 306,017 valid zero-rainfall observations
- 42.84% of valid observations recorded positive rainfall

## Distribution of valid rainfall observations

- Mean: 1.87 mm
- Median: 0.00 mm
- 95th percentile: 9.50 mm
- 99th percentile: 26.50 mm
- Raw maximum: 1,258 mm

The raw maximum is retained here as a data-quality warning rather than a research result. It should be checked against the source station, observation interval, and quality-control metadata before use. Negative sentinel values were excluded from all distribution statistics.

## Interpretation

The low valid-observation rate and frequent sentinel values explain why rain-gauge validation required explicit missing-data handling. The dataset supports analysis at substantial scale, but station availability and time alignment must be checked before comparing radar-derived rain-cell intensity with ground observations.

The repository contains synthetic examples rather than the complete 191 MB source dataset.

