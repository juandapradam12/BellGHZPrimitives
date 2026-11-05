"""
quantum_setup.py
----------------
Helper compartido para configurar el backend, transpilar el circuito
y preparar operadores ISA, tanto para simulador como para hardware real.

Elimina la duplicación de ~15 líneas de setup que existía en cada script
de EstimatorExecution y SamplerExecution.
"""
import importlib
import sys
import os

from qiskit.transpiler import generate_preset_pass_manager
from qiskit.providers.fake_provider import GenericBackendV2

# Rutas del proyecto calculadas una sola vez al importar el módulo
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(_PROJECT_ROOT, "src")


def _ensure_paths() -> None:
    """Añade las rutas necesarias a sys.path si no están ya presentes."""
    for path in [
        _PROJECT_ROOT,
        os.path.join(_SRC, "CircuitDefinition"),
        os.path.join(_SRC, "CircuitOptimization"),
    ]:
        if path not in sys.path:
            sys.path.insert(0, path)


def build_simulator_context(n_qubits: int) -> dict:
    """
    Crea el contexto completo para ejecución en simulador GenericBackendV2.

    Retorna un dict con:
        backend            — GenericBackendV2(n_qubits)
        qc                 — circuito GHZ original (sin transpilar, sin medidas)
        isa_circuit        — circuito transpilado al basis gate set del backend
        operators          — lista de operadores SparsePauliOp originales
        isa_operators_list — operadores con layout aplicado (para Estimator)
        observables_labels — etiquetas de texto de cada observable
    """
    _ensure_paths()
    mod = importlib.import_module("02_circuits_operators_optimization")

    backend = GenericBackendV2(num_qubits=n_qubits)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(mod.qc)
    isa_operators_list = [op.apply_layout(isa_circuit.layout) for op in mod.operators]

    return {
        "backend": backend,
        "qc": mod.qc,
        "isa_circuit": isa_circuit,
        "operators": mod.operators,
        "isa_operators_list": isa_operators_list,
        "observables_labels": mod.observables_labels,
    }


def build_hardware_context() -> dict:
    """
    Carga el contexto desde el módulo 02 para hardware real IBM Quantum.
    El backend y el circuito ya están transpilados en ese módulo.

    Retorna el mismo esquema de dict que build_simulator_context().
    """
    _ensure_paths()
    mod = importlib.import_module("02_circuits_operators_optimization")

    return {
        "backend": mod.backend,
        "qc": mod.qc,
        "isa_circuit": mod.isa_circuit,
        "operators": mod.operators,
        "isa_operators_list": mod.isa_operators_list,
        "observables_labels": mod.observables_labels,
    }


def add_measurements(qc, backend) -> object:
    """
    Crea una copia del circuito con medidas en todos los qubits y lo transpila
    para el backend dado. Necesario para el Sampler, que requiere medidas explícitas.

    Args:
        qc      — QuantumCircuit sin medidas
        backend — backend destino para la transpilación

    Returns:
        isa_circuit_meas — circuito transpilado con medidas
    """
    qc_meas = qc.copy()
    qc_meas.measure_all()
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    return pm.run(qc_meas)
