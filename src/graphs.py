import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Check if correct number of arguments are provided
if len(sys.argv) != 5:
    print(
        "Usage: python graphs.py <trace> <start_frames> <end_frames> <step_frames>"
    )
    sys.exit(1)

trace = sys.argv[1]
start_frames = int(sys.argv[2])
end_frames = int(sys.argv[3])
step_frames = int(sys.argv[4])

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

# Filter data for the specified trace
data = df[df['trace'] == trace]

# Calculate hit rate percentage (1 - fault_rate) * 100
data['hit_rate_percentage'] = (1 - data['fault_rate']) * 100

# Create the plot
plt.figure(figsize=(12, 8))  # Increase figure size for better resolution
for algorithm in data['algorithm'].unique():
    algo_data = data[data['algorithm'] == algorithm]
    plt.plot(algo_data['frames'],
             algo_data['hit_rate_percentage'],
             label=algorithm.upper(),
             linewidth=2)  # Increase line width

plt.title(f'Hit Rate vs Frame Size - {trace} Trace',
          fontsize=16)  # Increase font size
plt.xlabel('Number of Frames', fontsize=14)  # Increase font size
plt.ylabel('Hit Rate (%)',
           fontsize=14)  # Increase font size and add percentage sign
plt.grid(True)
plt.legend(fontsize=12)  # Increase font size

# Set x-axis ticks based on the provided range
plt.xticks(range(start_frames, end_frames + 1, step_frames),
           fontsize=12)  # Increase font size
plt.yticks(fontsize=12)  # Increase font size

# Save the figure with higher resolution
plt.savefig(os.path.join(graphs_dir, f'{trace}_hit_rate.png'), dpi=300)
plt.close()

print(f"Graph generated for {trace} trace in the 'graphs' directory.")
