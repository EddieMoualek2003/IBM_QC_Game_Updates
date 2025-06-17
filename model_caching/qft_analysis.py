import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from scipy.spatial.distance import jensenshannon
from scipy.special import rel_entr


number_qubits = 10

"""########################################################################
            Reading the Excel file into the program
"""
# The file that holds the results from the local, remote, and quantum runs
file_path = "qft_10_main.xlsx"  # replace with full path if needed
# Read the Excel file
df = pd.read_excel(file_path, dtype={'Binary': str})

"""########################################################################
            Process the DataFrame. This is done by:
                -> Grouping the data by 'Source' and 'Binary'
                -> Compensating for any missing states by padding with zeros
                -> Calculating the mean, probability, variance, and standard deviation for each group
                -> Converting the processed data into a new DataFrame
"""
# This will group the data by 'Source' and 'Binary', aggregating the 'Count'
groupedData = df.groupby(['Source', 'Binary'])['Count']
processed_df_list = []
for group_name, group_df in groupedData:
    # Since some of the processes require the data length to be 10, we need to ensure that the group_df has all 10 states.
    x = group_df.values.tolist()
    # Now, we need to work out the variance. This is a bit more involved because we need to account for different group sizes.
    if len(x) < 10:
        x += [0] * (10 - len(x))  # Pad with zeros if less than 10
    count_array = np.array(x)
    # print(f"{group_name}: The array of counts is {count_array}, with length {len(count_array)}")
    group_average = np.mean(count_array)
    group_probability = group_average / 4096  # Assuming 4096 is the total number of shots
    group_var = np.var(count_array)
    group_std = np.std(count_array)
    processed_df_list.append({
        'Source': group_name[0],
        'Bitstring': group_name[1],
        'Mean': group_average,
        'Probability': group_probability,
        'Variance': group_var,
        'StdDev': group_std,
        'MissingValues': 10 - len(group_df),
        'RawTotal': np.sum(count_array),
        'RawValues': x
    })
processed_df = pd.DataFrame(processed_df_list)


"""########################################################################
            Ensure All States Are Represented:
                -> There is a small chance that some states are not measured in any iteration of any source.
                -> We will ensure that all 1024 states are represented in the final DataFrame, for each source.
                -> If a state is missing, we will add it with a count of 0.
                    -> So far this has not been encountered, so it will be implemented when needed (mainly due to the lack of ability to properly test it.)
"""

# Generate all 10-bit binary strings
all_states = [''.join(bits) for bits in itertools.product('01', repeat=10)]

# Start by grouping data based on the source, and looking only at the Bitstring column.
groupedData = processed_df.groupby(['Source'])['Bitstring']
for group_name, group_df in groupedData:
    # print(f"Processing group: {group_name}")
    observed_bitstrings = set(group_df.values.tolist())
    missing_bitstrings = set(all_states) - observed_bitstrings
    if missing_bitstrings:
        print(f"Group {group_name} is missing {len(missing_bitstrings)} states.")
        print(f"Missing states: {sorted(missing_bitstrings)}")
    else:
        print(f"Group {group_name} has all expected bitstrings.")

complete_df = processed_df # Change this if corrections to the bitstring array need to be met.


"""########################################################################
            Now, we compare the data as groups based on the bitstrings:
                -> The data is grouped into bitstring groups.
                -> Each one will have three elements - one for each source.
                -> We will then average each bitstring, and pick the 3-5 most occuring ones,
                    -> These will form the basis for data analysis.
                    -> The others will be analysed for a general understanding/comparison between local and remote.
                -> Then, the relavent rows of the dataframe will be passed to plot things like a box and whisker plot.
"""

groupedData = complete_df.groupby(['Bitstring'])
average_mean_array = []
for group_name, group_df in groupedData:
    # print(f"Processing group: {group_name} - Data: \n{group_df}")
    
    bitstring_name = group_df['Bitstring'].values[0]
    average_mean = group_df['Mean'].mean()
    # print(f"Bitstring {bitstring_name} with mean: {average_mean}")
    average_mean_array.append([bitstring_name, average_mean])

sorted_mean_array = sorted_data = sorted(average_mean_array, key=lambda x: x[1], reverse=True)
selected_states = [pair[0] for pair in sorted_mean_array[0:4]]
if len(sorted_mean_array) == 2**number_qubits:
    print("All Elements Accounted For")


def plot_data(selected_states, complete_df, show_debug=False):
    """
    Plot box-and-whisker plots of RawValues for each selected bitstring,
    grouped by Source.

    Parameters:
    - selected_states: List of bitstrings (e.g., ['0000011111', '0000011110'])
    - complete_df: The full DataFrame containing 'Bitstring', 'Source', 'RawValues'
    - show_debug: If True, prints raw grouped data before plotting
    """

    # Filter to only selected bitstrings
    plotting_df = complete_df[complete_df['Bitstring'].isin(selected_states)].copy()

    # Debug output: print grouped data
    if show_debug:
        grouped = plotting_df.groupby('Bitstring')
        for group_name, group_df in grouped:
            print(f"\nProcessing group: {group_name} - Data:\n{group_df}")

    # Ensure RawValues is a list (parse if stored as string)
    plotting_df['RawValues'] = plotting_df['RawValues'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    # Explode the list of RawValues into separate rows
    exploded_df = plotting_df.explode('RawValues')
    exploded_df['RawValues'] = exploded_df['RawValues'].astype(float)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=exploded_df, x='Bitstring', y='RawValues', hue='Source')
    plt.title("Raw Count Distributions per Source for Selected States")
    plt.xlabel("Bitstring (State)")
    plt.ylabel("Raw Counts")
    plt.legend(title="Source")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def divergence_prep(complete_df):
    groupedData = complete_df.groupby(['Source'])['Mean']
    distribution = []
    for n, d in groupedData:
        distribution.append([n, d.values.tolist()])
    
    
    quantum_dist = distribution[1]
    print(quantum_dist)

    # for i in range(len(distribution))

    # print("JS(local || quantum):", js_divergence(local_dist, quantum_dist))
    # print("JS(remote || quantum):", js_divergence(remote_dist, quantum_dist))

    # print("KL(local || quantum):", kl_divergence(local_dist, quantum_dist))
    # print("KL(remote || quantum):", kl_divergence(remote_dist, quantum_dist))

    return 0

def js_divergence(p, q, base=2):
    """
    Calculate Jensen-Shannon divergence between two probability distributions.
    
    Returns a value between 0 and 1.
    """
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)

    # Normalize to make sure they're valid probability distributions
    p /= p.sum()
    q /= q.sum()

    js = jensenshannon(p, q, base=base)  # returns sqrt(JS)
    return js**2  # return actual JS divergence

def kl_divergence(p, q):
    """
    Calculate Kullback-Leibler divergence from p to q: D_KL(p || q).
    
    Note: p and q must be the same length and have no zero in q where p is non-zero.
    """
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)

    # Normalize to ensure probabilities
    p /= p.sum()
    q /= q.sum()

    # Smooth to avoid log(0) and division by 0
    eps = 1e-12
    p = np.clip(p, eps, 1)
    q = np.clip(q, eps, 1)

    return np.sum(rel_entr(p, q))  # = sum(p * log(p / q))


divergence_prep(complete_df)
