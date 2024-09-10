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

The `run_tests.sh` script supports three modes of operation:

1. Single trace, single algorithm:

```

./run_tests.sh <trace> <algorithm> <start_frames> <end_frames> <step_frames>

```

2. Single trace, all algorithms:

```

./run_tests.sh <trace> all <start_frames> <end_frames> <step_frames>

```

3. All traces, all algorithms:

```

./run_tests.sh all <start_frames> <end_frames> <step_frames>

```

Available traces: bzip, gcc, swim, sixpack
Available algorithms: rand, lru, clock

Frame parameters are optional. If not provided, default values are:

- start_frames: 10
- end_frames: 100
- step_frames: 10

This script will:

- Run the simulator for the specified trace(s) with the given algorithm(s) and frame range
- Save the results in `results.csv`
- Automatically call `graphs.py` to generate performance graph(s)

After the script completes, you'll find:

- `results.csv` in the project root, containing raw simulation data
- A `graphs/` directory containing PNG file(s) for the specified trace(s) and algorithm(s) combination(s)

## Example Usage

1. Run simulation for 'bzip' trace using 'rand' algorithm:

```

./run_tests.sh bzip rand 10 100 10

```

2. Run simulation for 'gcc' trace using all algorithms:

```

./run_tests.sh gcc all

```

3. Run simulation for all traces and all algorithms:

```

./run_tests.sh all

```

These commands will generate:

- A `results.csv` file with the simulation data
- Graph files in the `graphs/` directory showing the fault rate vs frame size for the specified configurations

## Viewing Results

- Raw data: Open `results.csv` to view detailed simulation results.
- Graphs: Check the `graphs/` directory for visual representations of fault rates vs frame sizes for the specified trace(s) and algorithm(s) combination(s).
