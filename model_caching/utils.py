from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit import transpile

## Module Imports
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.primitives import StatevectorSampler

def ibm_account_connect():
    token = "4Ke_JAy6uepzHTBV9fSDjGbFrSse7VYWwRgHJULxx34q"
    instance = "crn:v1:bluemix:public:quantum-computing:us-east:a/737dfb0b1e374ec7a5772fdbcece5643:a48276b9-a41b-449c-8d76-d2adf66ea9d4::"
    try:
        QiskitRuntimeService.save_account(
        token=token,
        channel="ibm_cloud", # `channel` distinguishes between different account types.
        instance=instance, # Copy the instance CRN from the Instance section on the dashboard.
        name="eddie_ibm_qc", # Optionally name this set of credentials.
        overwrite=True # Only needed if you already have Cloud credentials.
        )
    except:
        print("Account Exists - Continuing.")
    return None

def noisy_local_simulator(qc):
    # Use fake noisy backend
    fake_backend = FakeManilaV2()
    noise_model = NoiseModel.from_backend(fake_backend)
    simulator = AerSimulator(noise_model=noise_model)

    # Transpile circuit
    qc_t = transpile(qc, simulator)
    # Run simulation
    shots = 1024
    # Note: shots is set to 1024, but can be adjusted as needed.
    job = simulator.run(qc_t, shots=shots)
    result = job.result()
    counts = result.get_counts()
    return dict(sorted(counts.items(), key=lambda x: int(x[0], 2)))

def noisy_remote_simulator(qc):
    return qc

def ibm_quantum_backend(qc):
    ibm_account_connect()

    ## Run on the quantum computer.
    service = QiskitRuntimeService()
    backend = service.least_busy(simulator=False, operational=True, min_num_qubits=1)
    sampler = Sampler(mode=backend)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    ## Transpilation of the current circuit.
    isa_circuit = pm.run(qc)
    print("Circuit Transpiled")
    # print("Job Queued")
    ## Run the job on the quantum computer
    job = sampler.run([isa_circuit])
    pub_result = job.result()
    # print("Job Complete")

    return pub_result[0].data.c0.get_counts() # pub_result.data.meas.get_counts()


def prepare_measurements(qc, num_qubits):
    """Return three versions of the circuit with correct measurement syntax."""
    qc_local = qc.copy()
    qc_remote = qc.copy()
    qc_quantum = qc.copy()

    # Apply explicit measurement
    qc_local.measure(range(num_qubits), range(num_qubits))
    # qc_remote.measure(range(num_qubits), range(num_qubits))

    # measure_all auto-adds classical bits
    # qc_quantum.measure_all()

    return qc_local, qc_local, qc_local
