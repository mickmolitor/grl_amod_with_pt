# grl_amod_with_pt
This repository contains the codebase of my master's thesis. It is about the use of graph-based reinforcement learning for integrating autonomous on-demand services with regular public transportation.

## Run the application
To start the app, run the `main.py` file in the root directory. Based on your local device, this can be achieved via `py main.py` or `python3 main.py`. After startup, install all required packages to your local python installation with pip. After the application started, a menu will be displayed into your console. The first option will start the graph reinforcement learning algorithm either for the whole 21 day simulation period or a single day. The other three options are only important, when you want to  recreate some static data or for analysis purposes.

## Configure the application
Configuration can be done in the `params/program_params.py`. All parameters used in the masters thesis can be configured here. Initially shown is the standard parameter set.

# autonomous_on_demand_systems
Project on analytical information systems in the Information Systems masters program of Freie Universität Berlin. Research question: How can reinforcement learning approaches be used to optimize autonomous on-demand systems in public transport networks.

## Quick start with uv

Use uv for fast Python env and dependency management (Python 3.10+ per `pyproject.toml`).

1) Install uv globally

```bash
pip install uv
```

2) Create a virtual environment

```bash
uv venv
```

3) Activate the environment

- macOS/Linux:

```bash
source .venv/bin/activate
```

- Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

- Windows (CMD):

```bat
.venv\Scripts\activate.bat
```

4) Install project dependencies

```bash
uv sync
```