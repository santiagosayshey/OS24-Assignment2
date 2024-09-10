#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <trace> <algorithm> <start_frames> <end_frames> <step_frames>"
    echo "Available traces: bzip, gcc, swim, sixpack"
    echo "Available algorithms: rand, lru, clock"
    exit 1
fi

TRACE=$1
ALGORITHM=$2
START_FRAMES=$3
END_FRAMES=$4
STEP_FRAMES=$5

# Validate trace
if [[ ! " bzip gcc swim sixpack " =~ " $TRACE " ]]; then
    echo "Invalid trace. Available traces: bzip, gcc, swim, sixpack"
    exit 1
fi

# Validate algorithm
if [[ ! " rand lru clock " =~ " $ALGORITHM " ]]; then
    echo "Invalid algorithm. Available algorithms: rand, lru, clock"
    exit 1
fi

# Validate frame numbers
if ! [[ "$START_FRAMES" =~ ^[0-9]+$ ]] || ! [[ "$END_FRAMES" =~ ^[0-9]+$ ]] || ! [[ "$STEP_FRAMES" =~ ^[0-9]+$ ]]; then
    echo "Frame numbers must be integers"
    exit 1
fi

if [ "$START_FRAMES" -gt "$END_FRAMES" ]; then
    echo "Start frames must be less than or equal to end frames"
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Python interpreter and simulator script
SIMULATOR="python src/memsim.py"

# Output file
OUTPUT="results.csv"

# Create header for output file
echo "trace,algorithm,frames,page_faults,disk_reads,disk_writes,fault_rate" > $OUTPUT

# Run tests
for ((frames=START_FRAMES; frames<=END_FRAMES; frames+=STEP_FRAMES)); do
    echo "Running $TRACE with $ALGORITHM algorithm and $frames frames..."
    result=$($SIMULATOR "traces/${TRACE}.trace" $frames $ALGORITHM quiet)
    
    # Extract values from result
    page_faults=$(echo "$result" | grep "total disk reads:" | awk '{print $4}')
    disk_reads=$(echo "$result" | grep "total disk reads:" | awk '{print $4}')
    disk_writes=$(echo "$result" | grep "total disk writes:" | awk '{print $4}')
    fault_rate=$(echo "$result" | grep "page fault rate:" | awk '{print $4}')
    
    echo "$TRACE,$ALGORITHM,$frames,$page_faults,$disk_reads,$disk_writes,$fault_rate" >> $OUTPUT
done

echo "Tests completed. Results saved in $OUTPUT"

# Generate graph
python src/graphs.py $TRACE $ALGORITHM $START_FRAMES $END_FRAMES $STEP_FRAMES

# Deactivate the virtual environment
deactivate