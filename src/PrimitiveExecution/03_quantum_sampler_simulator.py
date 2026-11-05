"""
03_quantum_sampler_simulator.py
--------------------------------
Ejecuta el Sampler en un simulador GenericBackendV2.
Mide la distribución de bitstrings del estado GHZ.
Uso: python 03_quantum_sampler_simulator.py N_QUBITS=10 N_SHOTS=500
"""
import sys, os, csv

from qiskit_ibm_runtime.options_models import SamplerOptions
from qiskit_ibm_runtime.executor_sampler import Sampler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.config.env import N_SHOTS, N_QUBITS
from utils.visualization import plot_sampler_results
from utils.quantum_setup import build_simulator_context, add_measurements

# --- Setup compartido ---
ctx = build_simulator_context(N_QUBITS)
backend          = ctx["backend"]
isa_circuit_meas = add_measurements(ctx["qc"], backend)
print(f"Circuito cargado: {N_QUBITS} qubits | N_QUBITS={N_QUBITS}")

# --- Sampler ---
options = SamplerOptions()
options.default_shots = N_SHOTS
print(f">>> Shots configurados: {N_SHOTS}")

sampler = Sampler(backend, options=options)
job = sampler.run([(isa_circuit_meas,)])
print(f">>> Job ID: {job.job_id()}")

pub_result = job.result()[0]
bitstrings = pub_result.data.meas.get_bitstrings()

counts = {}
for b in bitstrings:
    counts[b] = counts.get(b, 0) + 1

# --- Print ---
print(f"\n--- Resultados Sampler (Simulator) ---")
print(f"Total shots: {N_SHOTS} | Estados únicos: {len(counts)}")
print(f"Primeros 10 bitstrings: {bitstrings[:10]}")
top = sorted(counts.items(), key=lambda x: -x[1])[:5]
print("\nTop 5 estados:")
for bs, cnt in top:
    print(f"  |{bs}⟩  {cnt:>5} veces  ({cnt/N_SHOTS*100:.1f}%)")

# --- CSV ---
suffix = f"{N_QUBITS}qubits_{N_SHOTS}shots"
csv_path = f"outputs/data/03_ghz_state_results_sampler_simulator_{suffix}.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["bitstring", "counts", "probability"])
    for bs, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        writer.writerow([bs, cnt, round(cnt / N_SHOTS, 6)])
print(f"\nCSV guardado en {csv_path}")

# --- Plot ---
plot_sampler_results(
    counts, n_shots=N_SHOTS, n_qubits=N_QUBITS,
    save_path=f"outputs/figures/03_ghz_state_results_sampler_simulator_{suffix}.png"
)
