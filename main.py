"""
main.py
--------
Punto de entrada principal del proyecto BellGHZPrimitives.

Recibe variables de configuración por CLI o variables de entorno y delega
la ejecución al script correspondiente según la primitiva y el modo elegidos.

Uso:
    python main.py [PRIMITIVE=estimator|sampler] [MODE=simulator|hardware] \\
                   [N_QUBITS=10] [N_SHOTS=500]

Ejemplos:
    python main.py                                          # estimator + simulator (defaults)
    python main.py PRIMITIVE=sampler N_QUBITS=5 N_SHOTS=200
    python main.py PRIMITIVE=estimator MODE=hardware N_QUBITS=2 N_SHOTS=100
    python main.py PRIMITIVE=sampler MODE=hardware N_QUBITS=2 N_SHOTS=100

Variables de entorno equivalentes (menor prioridad que CLI):
    PRIMITIVE=estimator|sampler
    MODE=simulator|hardware
    N_QUBITS=<int>
    N_SHOTS=<int>
"""
import sys
import os
import runpy

# --- Parseo de MODE (no está en arg_parser porque es exclusivo de main) ---
_VALID_MODES = {"simulator", "hardware"}
_DEFAULT_MODE = "simulator"


def _get_mode() -> str:
    for arg in sys.argv[1:]:
        if arg.startswith("MODE="):
            value = arg.split("=")[1].lower()
            if value not in _VALID_MODES:
                raise ValueError(f"MODE inválido: '{value}'. Usa: {_VALID_MODES}")
            return value
    env_value = os.getenv("MODE", _DEFAULT_MODE).lower()
    if env_value not in _VALID_MODES:
        raise ValueError(f"MODE inválido: '{env_value}'. Usa: {_VALID_MODES}")
    return env_value


# --- Añadir raíz al path antes de importar utils ---
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from utils.config.env import PRIMITIVE, N_QUBITS, N_SHOTS  # noqa: E402

MODE = _get_mode()

# --- Mapa de scripts ---
_SCRIPT_MAP = {
    ("estimator", "simulator"): "src/PrimitiveExecution/03_quantum_estimator_simulator.py",
    ("estimator", "hardware"):  "src/PrimitiveExecution/03_quantum_estimator_execution.py",
    ("sampler",   "simulator"): "src/PrimitiveExecution/03_quantum_sampler_simulator.py",
    ("sampler",   "hardware"):  "src/PrimitiveExecution/03_quantum_sampler_execution.py",
}

script_path = _SCRIPT_MAP.get((PRIMITIVE, MODE))
if script_path is None:
    print(f"❌ Combinación no soportada: PRIMITIVE={PRIMITIVE} MODE={MODE}")
    sys.exit(1)

script_abs = os.path.join(_ROOT, script_path)

print("=" * 55)
print(f"  BellGHZPrimitives — ejecutando primitiva")
print(f"  PRIMITIVE : {PRIMITIVE.upper()}")
print(f"  MODE      : {MODE.upper()}")
print(f"  N_QUBITS  : {N_QUBITS}")
print(f"  N_SHOTS   : {N_SHOTS}")
print(f"  Script    : {script_path}")
print("=" * 55)

runpy.run_path(script_abs, run_name="__main__")
