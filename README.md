# GDAPC-Dutta Data Projects

This repository collects practice materials for the Google Data Analytics
Professional Certificate. It includes a small Python package for exploring EPA
air-quality data as well as supporting artefacts for the Automatidata capstone
project. The codebase now provides a lightweight command-line script and a set
of reusable helper functions that demonstrate how to work with tabular data and
synthesise realistic mock datasets for experimentation.

## Repository structure

```
.
├── AirQuality_Analysis/
│   ├── ada_c2_labs.py          # Helper functions for EPA data labs
│   ├── c2_epa_air_quality.csv  # EPA air-quality sample dataset
│   └── Activity_ ... .ipynb    # Course notebooks
├── Automatidata Project/       # Reference documents and datasets
├── main.py                     # Command-line entry point for demos
└── README.md                   # Project documentation (this file)
```

## Getting started

### Prerequisites

- Python 3.10 or newer
- `pip` for managing Python packages

### Optional: Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Install dependencies

The interactive notebooks and helper functions rely on `pandas` and `numpy`.
Install them with:

```bash
pip install pandas numpy
```

## Usage

Run the demo script to preview the available utilities and datasets:

```bash
python main.py
```

Example output:

```
Hi, GDAPC community!
EPA Air Quality sample:
  - Alabama, Jefferson: AQI 48
  - Alabama, Jefferson: AQI 55
  - ...
Synthetic sales summary:
  - Customer 1: 2 purchases, total $74.10 ($32.12, $41.98)
  - ...
```

You can also use the helper functions directly within a notebook or another
application:

```python
from AirQuality_Analysis.ada_c2_labs import fetch_epa, lists_gen

states = fetch_epa("state")
verified_ids, feedback_ids = lists_gen(6, n_pool=500, n_feedback_ids=20, n_verified_ids=15)
```

## Development guidelines

- Keep functions annotated with type hints to clarify expected inputs and outputs.
- Prefer descriptive docstrings and concise inline comments for any non-obvious
  logic.
- Re-use the helper functions in `AirQuality_Analysis/ada_c2_labs.py` rather
  than duplicating logic when working with the EPA dataset.
- Before opening a pull request, run your preferred formatter and linter to
  maintain code quality.
