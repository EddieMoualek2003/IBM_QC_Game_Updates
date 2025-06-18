import pandas as pd

def data_logger(data, filename, num_qubits):


    # Flatten the data into long format
    rows = []
    for run_entry in data:
        run_num, run_data = run_entry
        for source, counts in run_data.items():
            for binary_key, value in counts.items():
                rows.append({
                    'Run': run_num,
                    'Source': source,
                    'Binary': binary_key,
                    'Count': value
                })

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Optional: sort by Run, then Source, then Binary
    df.sort_values(by=['Run', 'Source', 'Binary'], inplace=True)

    # Write to Excel
    filename_ext = str(filename.__name__) + "_" + str(num_qubits) + '.xlsx'
    df.to_excel(filename_ext, index=False)

            