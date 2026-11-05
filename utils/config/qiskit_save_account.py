from utils.config.env import qiskit_api_key, free_instance_crn
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    token=qiskit_api_key,
    instance=free_instance_crn,
)