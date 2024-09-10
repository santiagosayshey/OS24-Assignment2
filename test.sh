#!/bin/bash

# Function to run tests for a single trace and algorithm
run_single_test() {
    local trace=$1
    local algorithm=$2
    local start_frames=$3
    local end_frames=$4
    local step_frames=$5

    for ((frames=start_frames; frames<=end_frames; frames+=step_frames)); do
        echo "Running $trace with $algorithm algorithm and $frames frames..."
        result=$($SIMULATOR "traces/${trace}.trace" $frames $algorithm quiet)
        
        # Extract values from result
        page_faults=$(echo "$result" | grep "total disk reads:" | awk '{print $4}')
        disk_reads=$(echo "$result" | grep "total disk reads:" | awk '{print $4}')
        disk_writes=$(echo "$result" | grep "total disk writes:" | awk '{print $4}')
        fault_rate=$(echo "$result" | grep "page fault rate:" | awk '{print $4}')
        
        echo "$trace,$algorithm,$frames,$page_faults,$disk_reads,$disk_writes,$fault_rate" >> $OUTPUT
    done

    python src/graphs.py $trace $algorithm $start_frames $end_frames $step_frames
}

# Check if correct number of arguments are provided
if [ "$#" -lt 1 ] || [ "$#" -gt 5 ]; then
    echo "Usage:"
    echo "  $0 <trace> <algorithm> <start_frames> <end_frames> <step_frames>"
    echo "  $0 <trace> all <start_frames> <end_frames> <step_frames>"
    echo "  $0 all <start_frames> <end_frames> <step_frames>"
    echo "Available traces: bzip, gcc, swim, sixpack"
    echo "Available algorithms: rand, lru, clock"
    exit 1
fi

# Set default values for frames if not provided
START_FRAMES=${3:-10}
END_FRAMES=${4:-100}
STEP_FRAMES=${5:-10}

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

# Run tests based on input
if [ "$1" = "all" ]; then
    # Run all traces with all algorithms
    for trace in bzip gcc swim sixpack; do
        for algorithm in rand lru clock; do
            run_single_test $trace $algorithm $START_FRAMES $END_FRAMES $STEP_FRAMES
        done
    done
elif [ "$2" = "all" ]; then
    # Run all algorithms for a single trace
    TRACE=$1
    for algorithm in rand lru clock; do
        run_single_test $TRACE $algorithm $START_FRAMES $END_FRAMES $STEP_FRAMES
    done
else
    # Run a single trace with a single algorithm
    TRACE=$1
    ALGORITHM=$2
    run_single_test $TRACE $ALGORITHM $START_FRAMES $END_FRAMES $STEP_FRAMES
fi

echo "Tests completed. Results saved in $OUTPUT"

# Deactivate the virtual environment
deactivate