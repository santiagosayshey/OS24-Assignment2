#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Python interpreter and simulator script
SIMULATOR="python src/memsim.py"

# Traces to test
TRACES=("bzip" "gcc" "swim" "sixpack")

# Algorithms to test
ALGORITHMS=("rand" "lru" "clock")

# Range of frame numbers to test (adjust as needed)
START_FRAMES=10
END_FRAMES=100
STEP_FRAMES=10

# Output file
OUTPUT="results.csv"

# Create header for output file
echo "trace,algorithm,frames,page_faults,disk_reads,disk_writes,fault_rate" > $OUTPUT

# Run tests
for trace in "${TRACES[@]}"; do
    for algo in "${ALGORITHMS[@]}"; do
        for ((frames=START_FRAMES; frames<=END_FRAMES; frames+=STEP_FRAMES)); do
            echo "Running $trace with $algo algorithm and $frames frames..."
            result=$($SIMULATOR "traces/${trace}.trace" $frames $algo quiet)
            
            # Extract values from result
            page_faults=$(echo "$result" | grep "total disk reads:" | awk '{print $4}')
            disk_reads=$(echo "$result" | grep "total disk reads:" | awk '{print $4}')
            disk_writes=$(echo "$result" | grep "total disk writes:" | awk '{print $4}')
            fault_rate=$(echo "$result" | grep "page fault rate:" | awk '{print $4}')
            
            echo "$trace,$algo,$frames,$page_faults,$disk_reads,$disk_writes,$fault_rate" >> $OUTPUT
        done
    done
done

echo "Tests completed. Results saved in $OUTPUT"

# Generate graphs
python src/graphs.py

# Deactivate the virtual environment
deactivate