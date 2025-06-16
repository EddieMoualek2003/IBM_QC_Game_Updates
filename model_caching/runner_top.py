from qinb import qinb_main
from logger import data_logger
from qft_circuits import qft_3_main, qft_5_main, qft_10_main

run_list = [
    ["Quantum Interference Noise Benchmarking", qinb_main],
    ["QFT 3 Qubits", qft_3_main],
    ["QFT 5 Qubits", qft_5_main],
    ["QFT 10 Qubits", qft_10_main]
]


if __name__ == "__main__":
    for i, run in enumerate(run_list):
        print(f"{i}: {run[0]}")
    ## Instantiate the qinb_main function
    choice = int(input("Enter run option: ") or 0)

    counts_array = []
    for i in range(10):
        print("Running iteration", i + 1)
        counts = run_list[choice][1]()
        counts_array.append([i, counts])

    data_logger(counts_array, run_list[choice][1])