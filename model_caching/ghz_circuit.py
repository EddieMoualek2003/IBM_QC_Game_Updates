from qiskit import QuantumCircuit
from utils import *

def create_circuit(n=5):
    qc = QuantumCircuit(n, n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    qc.barrier()
    # qc.measure(range(n), range(n))
    return qc

def ghz_main(num_qubits):
    """Create and return a QFT circuit for 10 qubits."""
    # num_qubits = 25
    qc = create_circuit(num_qubits)
    qc_local, qc_remote, qc_quantum = prepare_measurements(qc, num_qubits)
    counts_local = noisy_local_simulator(qc_local)
    counts_remote = noisy_remote_simulator(qc_remote)
    counts_quantum = ibm_quantum_backend(qc_quantum)
    counts = {
        "local": counts_local,
        "remote_old_torino": counts_remote,
        "quantum": counts_quantum
    }
    return counts

def ghz_remote_main(num_qubits):
    """Create and return a QFT circuit for 10 qubits."""
    # num_qubits = 25
    qc = create_circuit(num_qubits)
    qc_local, qc_remote, qc_quantum = prepare_measurements(qc, num_qubits)

    counts_remote_torino = noisy_remote_simulator_2(qc_remote, "heron_model.pkl")
    counts_remote_brisbane = noisy_remote_simulator_2(qc_remote, "eagle_brisbane_model.pkl")
    counts_remote_sherbrooke = noisy_remote_simulator_2(qc_remote, "eagle_sherbrooke_model.pkl")
    counts = {
        "torino_remote": counts_remote_torino,
        "brisbane_remote": counts_remote_brisbane,
        "sherbrooke_remote": counts_remote_sherbrooke
    }
    return counts


