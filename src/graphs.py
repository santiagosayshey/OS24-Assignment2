import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Check if correct number of arguments are provided
if len(sys.argv) != 6:
    print(
        "Usage: python graphs.py <trace> <algorithm> <start_frames> <end_frames> <step_frames>"
    )
    sys.exit(1)

trace = sys.argv[1]
algorithm = sys.argv[2]
start_frames = int(sys.argv[3])
end_frames = int(sys.argv[4])
step_frames = int(sys.argv[5])

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (one level up from script_dir)
project_root = os.path.dirname(script_dir)

# Read the CSV file from the project root directory
df = pd.read_csv(os.path.join(project_root, 'results.csv'))

# Create a 'graphs' directory in the project root if it doesn't exist
graphs_dir = os.path.join(project_root, 'graphs')
if not os.path.exists(graphs_dir):
    os.makedirs(graphs_dir)

# Filter data for the specified trace and algorithm
data = df[(df['trace'] == trace) & (df['algorithm'] == algorithm)]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(data['frames'], data['fault_rate'])
plt.title(
    f'Fault Rate vs Frame Size - {trace} Trace, {algorithm.upper()} Algorithm')
plt.xlabel('Number of Frames')
plt.ylabel('Fault Rate')
plt.grid(True)

# Set x-axis ticks based on the provided range
plt.xticks(range(start_frames, end_frames + 1, step_frames))

# Save the figure
plt.savefig(os.path.join(graphs_dir, f'{trace}_{algorithm}_fault_rate.png'))
plt.close()

print(
    f"Graph generated for {trace} trace with {algorithm} algorithm in the 'graphs' directory."
)
