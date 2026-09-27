# Portfolio code

These scripts are cleaned, portable versions of analysis and visualization work developed during the NTU rain-cell research project. They are separated from the upstream tracking engine so that the author's individual contributions can be reviewed without republishing the UK Met Office codebase.

Included:

- `select_events.py`: identify sustained high-reflectivity events from HDF5 radar files.
- `visualize_tracks.py`: render exported GeoJSON rain-cell tracks and optionally create a GIF.
- `summarize_fallbacks.py`: summarize fallback usage in exported track GeoJSON files.

Not included:

- The UK Met Office MO-cell-tracking engine.
- Raw radar, satellite, rain-gauge, or laboratory datasets.
- Laboratory infrastructure paths or credentials.

The scripts expect authorized local inputs supplied by the user. Run each script with `--help` for its interface.

