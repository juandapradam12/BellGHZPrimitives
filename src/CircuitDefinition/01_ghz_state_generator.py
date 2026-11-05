from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
import sys, os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # raíz del proyecto
from utils.config.arg_parser import get_n_qubits

def get_qc_for_n_qubit_GHZ_state(n: int) -> QuantumCircuit:
    """This function will create a qiskit.QuantumCircuit (qc)
        for an n-qubit GHZ state.

    Args:
        n (int): Number of qubits in the n-qubit GHZ state

    Returns:
        QuantumCircuit: Quantum circuit that generate the n-qubit GHZ state,
            assuming all qubits start in the 0 state
    """
    if isinstance(n, int) and n >= 2:
        qc = QuantumCircuit(n)
        qc.h(0)
        for i in range(n - 1):
            qc.cx(i, i + 1)
    else:
        raise Exception("n is not a valid input")
    return qc


# Número de qubits leído desde argumento N_QUBITS (debe ser > 2)
n = get_n_qubits()
qc = get_qc_for_n_qubit_GHZ_state(n)

fig = qc.draw("mpl")
fig.savefig("Outputs/figures/01_bell_state_circuit.png", dpi=150, bbox_inches="tight")
plt.show()

# ZZII...II, ZIZI...II, ... , ZIII...IZ
operator_strings = [
    "Z" + "I" * i + "Z" + "I" * (n - 2 - i) for i in range(n - 1)
]

operators = [SparsePauliOp(operator) for operator in operator_strings]