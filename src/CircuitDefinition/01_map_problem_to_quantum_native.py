from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from matplotlib import pyplot as plt

# Legacy server-side primitive before qiskit-ibm-runtime 0.50.0
# from qiskit_ibm_runtime import EstimatorOptions
# from qiskit_ibm_runtime import Estimator

# Uncomment the next line if you want to use a simulator:
# from qiskit_ibm_runtime.fake_provider import FakeBelemV2


# Create a new circuit with two qubits
qc = QuantumCircuit(2)

# Add a Hadamard gate to qubit 0
qc.h(0)

# Perform a controlled-X gate on qubit 1, controlled by qubit 0
qc.cx(0, 1)

# Return a drawing of the circuit using MatPlotLib ("mpl").
# These guides are written by using Jupyter notebooks, which
# display the output of the last line of each cell.
# If you're running this in a script, use `print(qc.draw())` to
# print a text drawing.
fig = qc.draw("mpl")
fig.savefig("Outputs/figures/01_bell_state_circuit.png", dpi=150, bbox_inches="tight")
plt.show()

# Set up six different observables
observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
observables = [SparsePauliOp(label) for label in observables_labels]