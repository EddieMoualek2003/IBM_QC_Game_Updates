from qiskit import QuantumCircuit
from utils import *

def create_qft_circuit(num_qubits):
    """Generate a QFT circuit for a given number of qubits."""
    qc = QuantumCircuit(num_qubits, num_qubits)
    for j in range(num_qubits):
        qc.h(j)
        for k in range(j + 1, num_qubits):
            angle = 3.141592653589793 / (2 ** (k - j))
            qc.cp(angle, k, j)
    qc.barrier()
    for i in range(num_qubits // 2):
        qc.swap(i, num_qubits - i - 1)
    return qc


def qft_10_main():
    """Create and return a QFT circuit for 10 qubits."""
    num_qubits = 10
    qc = create_qft_circuit(num_qubits)
    qc_local, qc_remote, qc_quantum = prepare_measurements(qc, num_qubits)
    counts_local = noisy_local_simulator(qc_local)
    counts_remote = noisy_remote_simulator(qc_remote)
    counts_quantum = ibm_quantum_backend(qc_quantum)
    counts = {
        "local": counts_local,
        "remote": counts_remote,
        "quantum": counts_quantum
    }
    return counts

def qft_5_main():
    """Create and return a QFT circuit for 5 qubits."""
    num_qubits = 5
    qc = create_qft_circuit(num_qubits)
    qc_local, qc_remote, qc_quantum = prepare_measurements(qc, num_qubits)
    counts_local = noisy_local_simulator(qc_local)
    counts_remote = noisy_remote_simulator(qc_remote)
    counts_quantum = ibm_quantum_backend(qc_quantum)
    counts = {
        "local": counts_local,
        "remote": counts_remote,
        "quantum": counts_quantum
    }
    return counts

def qft_3_main():
    """Create and return a QFT circuit for 3 qubits."""
    num_qubits = 3
    qc = create_qft_circuit(num_qubits)
    qc_local, qc_remote, qc_quantum = prepare_measurements(qc, num_qubits)
    counts_local = noisy_local_simulator(qc_local)
    counts_remote = noisy_remote_simulator(qc_remote)
    counts_quantum = ibm_quantum_backend(qc_quantum)
    counts = {
        "local": counts_local,
        "remote": counts_remote,
        "quantum": counts_quantum
    }
    return counts
