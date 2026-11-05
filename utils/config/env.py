import os
from dotenv import load_dotenv
from utils.config.arg_parser import get_n_qubits, get_n_shots, get_primitive, DEFAULT_SHOTS

load_dotenv()

# IBM Quantum credentials
qiskit_api_key = os.getenv("QISKIT_API_KEY")
free_instance_crn = os.getenv("FREE_INSTANCE_CRN")

# Runtime parameters
N_QUBITS = get_n_qubits()
N_SHOTS = get_n_shots() or DEFAULT_SHOTS
PRIMITIVE = get_primitive()
