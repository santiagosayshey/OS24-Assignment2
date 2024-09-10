# Virtual Memory Simulator

This project simulates various page replacement algorithms for virtual memory management. It includes implementations of Random, LRU, and Clock algorithms, and provides tools to analyze their performance across different memory traces.

## Repository Structure

- `src/`
  - `memsim.py`: The main simulator implementation
  - `graphs.py`: Script to generate performance graphs
- `traces/`: Directory containing memory trace files
- `run_tests.sh`: Shell script to run simulations and generate results
- `requirements.txt`: List of Python dependencies
- `venv/`: Virtual environment directory (created during setup)

## Setup

1. Run the setup script to create a python environment. This will install all requirements:

```
chmod +x setup.sh
./setup.sh
```

## Running Tests and Generating Graphs

The `run_tests.sh` script supports two modes of operation:

1. Single trace:

```
./run_tests.sh <trace> <start_frames> <end_frames> <step_frames>
```

2. All traces:

```
./run_tests.sh all <start_frames> <end_frames> <step_frames>
```

Available traces: bzip, gcc, swim, sixpack

Frame parameters are optional. If not provided, default values are:

- start_frames: 0
- end_frames: 20
- step_frames: 1

This script will:

- Run the simulator for the specified trace(s) with all algorithms (rand, lru, clock) and the given frame range
- Save the results in `results.csv`
- Automatically call `graphs.py` to generate performance graph(s)

After the script completes, you'll find:

- `results.csv` in the project root, containing raw simulation data
- A `graphs/` directory containing PNG file(s) for the specified trace(s), showing the fault rate vs frame size for all algorithms

## Example Usage

1. Run simulation for 'bzip' trace:

```
./run_tests.sh bzip 0 20 1
```

2. Run simulation for all traces:

```
./run_tests.sh all
```

These commands will generate:

- A `results.csv` file with the simulation data
- Graph files in the `graphs/` directory showing the fault rate vs frame size for all algorithms for the specified trace(s)

## Viewing Results

- Raw data: Open `results.csv` to view detailed simulation results.
- Graphs: Check the `graphs/` directory for visual representations of fault rates vs frame sizes for all algorithms for the specified trace(s).
