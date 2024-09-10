import pandas as pd
import matplotlib.pyplot as plt
import os

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

# Create a plot for each trace and each algorithm
for trace in df['trace'].unique():
    for algorithm in df['algorithm'].unique():
        plt.figure(figsize=(10, 6))

        # Filter data for the current trace and algorithm
        data = df[(df['trace'] == trace) & (df['algorithm'] == algorithm)]

        # Plot fault rate vs frame size
        plt.plot(data['frames'], data['fault_rate'])

        plt.title(
            f'Fault Rate vs Frame Size - {trace} Trace, {algorithm.upper()} Algorithm'
        )
        plt.xlabel('Number of Frames')
        plt.ylabel('Fault Rate')
        plt.grid(True)

        # Save the figure
        plt.savefig(
            os.path.join(graphs_dir, f'{trace}_{algorithm}_fault_rate.png'))
        plt.close()

print(
    "12 graphs generated (one for each algorithm for each trace) in the 'graphs' directory."
)
