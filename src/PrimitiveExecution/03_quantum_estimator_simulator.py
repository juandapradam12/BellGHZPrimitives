"""
03_quantum_estimator_simulator.py
----------------------------------
Ejecuta el Estimator en un simulador GenericBackendV2.
Uso: python 03_quantum_estimator_simulator.py N_QUBITS=10 N_SHOTS=500
"""
import sys, os, csv

from qiskit_ibm_runtime.options_models import EstimatorOptions
from qiskit_ibm_runtime.executor_estimator import Estimator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.config.env import N_SHOTS, N_QUBITS
from utils.visualization import plot_estimator_results, plot_ghz_decay
from utils.helpers.quantum_setup import build_simulator_context

# --- Setup compartido ---
ctx = build_simulator_context(N_QUBITS)
backend            = ctx["backend"]
isa_circuit        = ctx["isa_circuit"]
isa_operators_list = ctx["isa_operators_list"]
observables_labels = ctx["observables_labels"]
print(f"Circuito cargado: {N_QUBITS} qubits | N_QUBITS={N_QUBITS}")

# --- Estimator ---
options = EstimatorOptions()
options.resilience_level = 1
options.default_shots = N_SHOTS
print(f">>> Shots configurados: {N_SHOTS}")

estimator = Estimator(backend, options=options)
job = estimator.run([(isa_circuit, isa_operators_list)])
print(f">>> Job ID: {job.job_id()}")

pub_result = job.result()[0]
evs  = pub_result.data.evs
stds = pub_result.data.stds

# --- Print ---
print("\n--- Resultados Estimator (Simulator) ---")
print(f"{'Observable':<12} {'Valor esperado':>16} {'± Std':>10}")
print("-" * 42)
for label, ev, std in zip(observables_labels, evs, stds):
    print(f"{label:<12} {ev:>16.4f} {std:>10.4f}")

# --- CSV ---
suffix = f"{N_QUBITS}qubits_{N_SHOTS}shots"
csv_path = f"outputs/data/03_bell_state_results_estimator_simulator.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["observable", "expected_value", "std", "n_qubits", "n_shots"])
    for label, ev, std in zip(observables_labels, evs, stds):
        writer.writerow([label, round(float(ev), 6), round(float(std), 6), N_QUBITS, N_SHOTS])
print(f"\nCSV guardado en {csv_path}")

# --- Plots ---
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
