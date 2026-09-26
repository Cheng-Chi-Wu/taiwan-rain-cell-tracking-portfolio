# Taiwan Rain-Cell Tracking and Thunderstorm Analysis

An applied data-science research project that adapts a multi-object cell-tracking workflow to Taiwan radar data and evaluates afternoon-thunderstorm events using radar, rain-gauge, satellite, and event records.

> **Repository status:** This is a portfolio-oriented research summary. The underlying tracking system was adapted from the UK Met Office MO-cell-tracking codebase. Its upstream licensing and laboratory data-sharing permissions are still being confirmed, so the full modified source code and raw datasets are not included in this initial private release.

## Research question

Afternoon thunderstorms in Taiwan are spatially localized, short-lived, and intense. Their short lead times make urban flood response difficult. This project investigates whether radar-derived rain-cell tracks and satellite observations can support earlier and more reliable event characterization.

## What I worked on

- Adapted the cell-tracking workflow to Taiwan-specific grids, UTC+8 timestamps, radar resolution, VIL thresholds, and smoothing parameters.
- Processed HDF5 radar products with Python, NumPy, SciPy, and Matplotlib.
- Identified and tracked rain cells across consecutive radar frames and visualized tracks on Taiwan maps.
- Integrated radar observations, rain-gauge measurements, satellite channels, and event records.
- Diagnosed missing-frame, temporal-alignment, spatial-resolution, and measurement-scale issues.
- Investigated `Zero weight for featId` failures in forward/backward track association.
- Implemented and evaluated a fallback association strategy while comparing track recovery against trajectory-quality risk.
- Tested parameter combinations including VIL thresholds, smoothing width, minimum area, and matching-distance constraints.

## Workflow

1. Collect documented afternoon-thunderstorm events.
2. Load 10-minute radar observations and extract rain-cell features.
3. Project detected cells onto a Taiwan grid and associate features across time.
4. Compare radar-derived signals with nearby rain gauges and satellite channels.
5. Diagnose failed associations and apply a marked fallback strategy only when needed.
6. Compare parameter settings using detected-track counts, fallback frequency, and visual trajectory quality.

## Selected results

### Rain-cell detection and mapping

![Rain-cell tracking result](docs/images/rain-cell-result.png)

### Parameter and fallback evaluation

![Fallback and parameter comparison](docs/images/parameter-comparison.png)

### Satellite and observation comparison

![Satellite comparison](docs/images/satellite-comparison.png)

The experiments show a recurring trade-off: relaxing association distance can recover more tracks but increases the risk of incorrect matching. A targeted, explicitly labeled fallback method preserves the stricter default matching logic while making exceptional cases measurable during later quality analysis.

## Tools

- Python
- NumPy, Pandas, SciPy
- Matplotlib
- HDF5 / h5py
- GeoJSON and geospatial projection tools
- Linux, Conda, Git

## Research materials

- [Research presentation](docs/Rain_Cell_research_report.pdf)
- [Research poster source](docs/Rain_Cell_research_poster.pptx)

## Reproducibility and data availability

Raw radar, satellite, rain-gauge, and laboratory data are not included. A future public release will add a small authorized sample or synthetic dataset, reproducible analysis scripts, environment specifications, and tests after licensing and data-sharing review.

## Attribution

The tracking workflow was adapted from the UK Met Office MO-cell-tracking codebase for research use in Taiwan. This repository does not claim authorship of the upstream tracking system. The project contributions described here concern Taiwan-specific adaptation, data integration, failure analysis, fallback evaluation, parameter experiments, and research communication.

## Author

Cheng-Chi Wu  
MEng in Data Science, UCLA  
B.S. in Civil Engineering, National Taiwan University

