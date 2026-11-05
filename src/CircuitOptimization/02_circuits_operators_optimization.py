import importlib, sys, os
import matplotlib.pyplot as plt

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler import generate_preset_pass_manager

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # raíz del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "CircuitDefinition"))  # 01_*

from utils.config.env import N_QUBITS

# --- Selección de circuito según N_QUBITS ---
# Uso: python3 02_circuits_operators_optimization.py N_QUBITS=100
# Si no se pasa argumento o N_QUBITS <= 2 → caso base (Bell State)
# Si N_QUBITS > 2 → GHZ State

if N_QUBITS > 2:
    module = importlib.import_module("01_ghz_state_generator")
    qc = module.qc
    operators = module.operators
    observables_labels = module.operator_strings
else:
    module = importlib.import_module("01_map_problem_to_quantum_native")
    qc = module.qc
    operators = module.observables
    observables_labels = module.observables_labels

print(f"Circuito cargado: {qc.num_qubits} qubits | N_QUBITS={N_QUBITS}")

service = QiskitRuntimeService()

backend = service.least_busy(
    simulator=False, operational=True, min_num_qubits=N_QUBITS
)

# Convert to an ISA circuit and layout-mapped observables.
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
isa_circuit = pm.run(qc)
isa_operators_list = [op.apply_layout(isa_circuit.layout) for op in operators]

fig = isa_circuit.draw("mpl", idle_wires=False)
fig.savefig("outputs/figures/02_isa_circuit.png", dpi=150, bbox_inches="tight")
plt.show()