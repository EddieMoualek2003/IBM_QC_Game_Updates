from qinb import qinb_main
from logger import data_logger

run_list = [
    ["Quantum Interference Noise Benchmarking", qinb_main],

]


if __name__ == "__main__":
    for i, run in enumerate(run_list):
        print(f"{i}: {run[0]}")
    ## Instantiate the qinb_main function
    choice = int(input("Enter run option: ") or 0)

    counts_array = []
    for i in range(5):
        counts = run_list[choice][1]()
        counts_array.append([i, counts])

    data_logger(counts_array, qinb_main)