import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon
from scipy.special import rel_entr

def process_sheets():
    # Load the Excel file
    file_path = "qinb_main.xlsx"  # replace with full path if needed
    df = pd.read_excel(file_path, dtype={'Binary': str})

    # Clean 'Count' column if it contains commas (e.g., '1,132')
    if df['Count'].dtype == object:
        df['Count'] = df['Count'].str.replace(',', '').astype(int)

    df['Probability'] = df['Count'] / 4096

    # Extract binary and source options
    binary_options = df['Binary'].unique().tolist()
    source_options = df['Source'].unique()
    print("Binary options:", binary_options)
    print("Source options:", source_options)

    data_to_write = []

    for binary in binary_options:
        for source in source_options:
            filtered_df = df[(df['Binary'] == binary) & (df['Source'] == source)]
            average_prob = filtered_df['Probability'].mean() if not filtered_df.empty else 0
            instance_var = filtered_df['Probability'].var() if not filtered_df.empty else 0
            instance_dev = filtered_df['Probability'].std() if not filtered_df.empty else 0
            data_array = [binary, source, average_prob, instance_var, instance_dev]
            data_to_write.append(data_array)

    # Process divergence metrics
    divergence_data = divergence_metrics(data_to_write)
    return data_to_write


def divergence_metrics(data):
    # Organize data by source and binary state
    mean_prob = {'local': {}, 'remote': {}, 'quantum': {}}
    stds = {'local': {}, 'remote': {}, 'quantum': {}}
    stderrs = {'local': {}, 'remote': {}, 'quantum': {}}

    for state, source, mean, std, stderr in data:
        mean_prob[source][state] = mean
        stds[source][state] = std
        stderrs[source][state] = stderr

    # Ensure all keys are aligned (sorted for consistent order)
    all_states = sorted(mean_prob['quantum'].keys())

    # Convert to NumPy arrays
    local_values = np.array([mean_prob['local'].get(k, 0.0) for k in all_states], dtype=float)
    remote_values = np.array([mean_prob['remote'].get(k, 0.0) for k in all_states], dtype=float)
    quantum_values = np.array([mean_prob['quantum'].get(k, 0.0) for k in all_states], dtype=float)

    # KL Divergence (handle zeros with epsilon)
    epsilon = 1e-10
    local_kl = np.sum(rel_entr(local_values + epsilon, quantum_values + epsilon))
    remote_kl = np.sum(rel_entr(remote_values + epsilon, quantum_values + epsilon))

    # Jensen-Shannon Divergence
    js_local = jensenshannon(local_values, quantum_values, base=2)
    js_remote = jensenshannon(remote_values, quantum_values, base=2)

    print("\n--- Divergence Metrics ---")
    print("Local KL Divergence:", local_kl)
    print("Remote KL Divergence:", remote_kl)
    print("Local Jensen-Shannon Divergence:", js_local)
    print("Remote Jensen-Shannon Divergence:", js_remote)

    return local_kl, remote_kl


# Optional: KL function (no longer used, but included for reference)
def kl_divergence(p, q, epsilon=1e-10):
    all_keys = set(p) | set(q)
    kl = 0.0
    for key in all_keys:
        p_val = p.get(key, 0.0) + epsilon
        q_val = q.get(key, 0.0) + epsilon
        kl += p_val * np.log(p_val / q_val)
    return kl


# Run the processing function
if __name__ == "__main__":
    processed_data = process_sheets()
