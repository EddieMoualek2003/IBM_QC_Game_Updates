from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer.noise import NoiseModel
import pickle

def cache_noise_model(backend_name, filename):
    service = QiskitRuntimeService(name="eddie_ibm_qc")  # use your account name
    backend = service.backend(backend_name)

    noise_model = NoiseModel.from_backend(backend)

    with open(filename, "wb") as f:
        pickle.dump(noise_model, f)

    print(f"Noise model from {backend_name} saved to {filename}")

cache_noise_model("ibm_torino", "cached_noise_model.pkl")