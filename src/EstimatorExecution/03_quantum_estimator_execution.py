import importlib, sys, os
import csv

# Client-side primitive introduced in qiskit-ibm-runtime 0.50.0
from qiskit_ibm_runtime.options_models import EstimatorOptions
from qiskit_ibm_runtime.executor_estimator import Estimator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # raíz del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "CircuitOptimization"))  # 02_*

from utils.visualization import plot_estimator_results, plot_ghz_decay
from utils.config.env import N_SHOTS, N_QUBITS

module = importlib.import_module("02_circuits_operators_optimization")

backend = module.backend
isa_circuit = module.isa_circuit
isa_operators_list = module.isa_operators_list

# Construct the Estimator instance with error suppression (dynamical decoupling)
options = EstimatorOptions()
options.resilience_level = 1
options.dynamical_decoupling.enable = True
options.dynamical_decoupling.sequence_type = "XY4"

options.default_shots = N_SHOTS
print(f">>> Shots configurados: {N_SHOTS}")

estimator = Estimator(backend, options=options)

# Submit the circuit to Estimator
job = estimator.run([(isa_circuit, isa_operators_list)])
job_id = job.job_id()
print(f">>> Job ID: {job_id}")

# This is the result of the entire submission.  You submitted one Pub,
# so this contains one inner result (and some metadata of its own).
job_result = job.result()
print("Job Result")
print(job_result)

# This is the result from our single pub, which had six observables,
# so contains information on all six.
pub_result = job.result()[0]

# Imprimir resultados de forma legible
observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
evs  = pub_result.data.evs
stds = pub_result.data.stds

print("\n--- Resultados del Bell State (Q Hardware) ---")
print(f"{'Observable':<12} {'Valor esperado':>16} {'± Std':>10}")
print("-" * 42)
for label, ev, std in zip(observables_labels, evs, stds):
    print(f"{label:<12} {ev:>16.4f} {std:>10.4f}")

# --- Guardar CSV ---
suffix = f"{N_QUBITS}qubits_{N_SHOTS}shots"
csv_path = f"Outputs/data/03_bell_state_results_estimator_q_hardware_{suffix}.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["observable", "expected_value", "std"])
    for label, ev, std in zip(observables_labels, evs, stds):
        writer.writerow([label, round(float(ev), 6), round(float(std), 6)])
print(f"\nCSV guardado en {csv_path}")

# --- Visualización ---
plot_estimator_results(
    observables_labels, evs, stds,
    save_path=f"Outputs/figures/03_bell_state_results_estimator_q_hardware_{suffix}.png"
)

if N_QUBITS > 2:
    plot_ghz_decay(
        evs, n_qubits=N_QUBITS,
        label="GHZ state (Q Hardware)",
        save_path=f"Outputs/figures/03_ghz_decay_estimator_q_hardware_{suffix}.png"
    )