
import importlib, sys, os
import csv
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.options_models import EstimatorOptions
from qiskit_ibm_runtime.executor_estimator import Estimator
from qiskit.providers.fake_provider import GenericBackendV2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # raíz del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "CircuitDefinition"))   # 01_*
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "CircuitOptimization")) # 02_*

from utils.visualization import plot_estimator_results, plot_ghz_decay
from utils.config.env import N_SHOTS, N_QUBITS

# Importar el circuito original (sin transpilar) y operadores desde módulo 02
module_02 = importlib.import_module("02_circuits_operators_optimization")
qc = module_02.qc
operators = module_02.operators
observables_labels = module_02.observables_labels

# Simulador GenericBackendV2 — transpila el circuito para su propio basis gate set
backend = GenericBackendV2(num_qubits=N_QUBITS)

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
isa_operators_list = [op.apply_layout(isa_circuit.layout) for op in operators]

options = EstimatorOptions()
options.resilience_level = 1
options.default_shots = N_SHOTS
print(f">>> Shots configurados: {N_SHOTS}")

estimator = Estimator(backend, options=options)

# Submit the circuit to Estimator
job = estimator.run([(isa_circuit, isa_operators_list)])
job_id = job.job_id()
print(f">>> Job ID: {job_id}")

# This is the result of the entire submission. You submitted one Pub,
# so this contains one inner result (and some metadata of its own).
job_result = job.result()
print("Job Result")
print(job_result)

# This is the result from our single pub, which had six observables,
# so contains information on all six.
pub_result = job.result()[0]

# Imprimir resultados de forma legible
evs  = pub_result.data.evs
stds = pub_result.data.stds

print("\n--- Resultados (Simulator) ---")
print(f"{'Observable':<12} {'Valor esperado':>16} {'± Std':>10}")
print("-" * 42)
for label, ev, std in zip(observables_labels, evs, stds):
    print(f"{label:<12} {ev:>16.4f} {std:>10.4f}")

# --- Guardar CSV ---
suffix = f"{N_QUBITS}qubits_{N_SHOTS}shots"
csv_path = f"outputs/data/03_bell_state_results_estimator_simulator_{suffix}.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["observable", "expected_value", "std"])
    for label, ev, std in zip(observables_labels, evs, stds):
        writer.writerow([label, round(float(ev), 6), round(float(std), 6)])
print(f"\nCSV guardado en {csv_path}")

# --- Visualizacion ---
plot_estimator_results(
    observables_labels, evs, stds,
    save_path=f"outputs/figures/03_bell_state_results_estimator_simulator_{suffix}.png"
)

if N_QUBITS > 2:
    plot_ghz_decay(
        evs, n_qubits=N_QUBITS,
        label="GHZ state (Simulator)",
        save_path=f"outputs/figures/03_ghz_decay_estimator_simulator_{suffix}.png"
    )
