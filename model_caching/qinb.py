"""
QINB: Quantum Interference Noise Benchmarking
    -> This script benchmarks the noise in quantum circuits by simulating interference effects.
    -> It will be benchmarked across three methods of execution:
    1. Local noisy simulator
    2. Remote noisy simulator
    3. IBM Quantum backend
"""


from qiskit import QuantumCircuit
from matplotlib import pyplot as plt
from utils import *

def qinb_circuit_creation():

    # Create circuit
    qc = QuantumCircuit(3, 3)

    # Step 1: Create superposition
    qc.h(0)
    qc.h(1)

    # Step 2: Apply controlled phase shift (simulate interference)
    qc.cp(0.5 * 3.1415, 0, 1)  # CP(pi/2)
    qc.h(1)
    qc.cx(1, 2)
    qc.h(2)

    # Step 3: Add more phase entanglement
    qc.cp(3.1415, 0, 2)  # CP(pi)

    # Step 4: Final Hadamard for interference
    qc.h(0)
    qc.h(1)
    qc.h(2)

    # Prepare measurements
    return prepare_measurements(qc, 3)

def qinb_main():
    """Main function to run the QINB circuit and return counts."""
    qc_local, qc_remote, qc_quantum = qinb_circuit_creation()
    counts_local = noisy_local_simulator(qc_local)
    counts_remote = noisy_remote_simulator(qc_remote)
    counts_quantum = ibm_quantum_backend(qc_quantum)
    counts = {
        "local": counts_local,
        "remote": counts_remote,
        "quantum": counts_quantum
    }
    return counts
