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

1. Run the test script with specific parameters:

```
chmod +x test.sh
./run_test.sh <trace> <algorithm> <start_frames> <end_frames> <step_frames>

```

Available traces: bzip, gcc, swim, sixpack
Available algorithms: rand, lru, clock

This script will:

- Run the simulator for the specified trace file with the given algorithm and frame range
- Save the results in `results.csv`
- Automatically call `graphs.py` to generate a performance graph

2. After the script completes, you'll find:

- `results.csv` in the project root, containing raw simulation data
- A `graphs/` directory containing a PNG file for the specified trace and algorithm combination

## Example Usage

To run the simulation for the 'bzip' trace using the 'rand' algorithm, with frames starting at 10, ending at 100, and incrementing by 10:

```

./run_tests.sh bzip rand 10 100 10

```

This will generate:

- A `results.csv` file with the simulation data
- A graph file `graphs/bzip_rand_fault_rate.png` showing the fault rate vs frame size for this specific configuration

## Viewing Results

- Raw data: Open `results.csv` to view detailed simulation results.
- Graphs: Check the `graphs/` directory for visual representations of fault rates vs frame sizes for the specified trace and algorithm combination.
