import sys

DEFAULT_SHOTS = 100  # default interno seguro para hardware real
DEFAULT_PRIMITIVE = "estimator"
VALID_PRIMITIVES = {"estimator", "sampler"}


def get_n_qubits() -> int:
    """
    Parsea el argumento N_QUBITS desde la línea de comandos.
    Uso: python3 script.py N_QUBITS=100
    Si no se pasa o N_QUBITS <= 2 retorna 2 (caso base).
    """
    n_qubits = 2
    for arg in sys.argv[1:]:
        if arg.startswith("N_QUBITS="):
            n_qubits = int(arg.split("=")[1])
    return n_qubits


def get_n_shots() -> int | None:
    """
    Parsea el argumento N_SHOTS desde la línea de comandos.
    Uso: python3 script.py N_SHOTS=5000
    Si no se pasa retorna None (usa el default del backend).
    """
    for arg in sys.argv[1:]:
        if arg.startswith("N_SHOTS="):
            return int(arg.split("=")[1])
    return None


def get_primitive() -> str:
    """
    Parsea el argumento PRIMITIVE desde la línea de comandos o variable de entorno.
    Uso: python main.py PRIMITIVE=sampler
    Valores válidos: estimator | sampler
    Si no se pasa, retorna el default 'estimator'.
    """
    import os
    # CLI tiene prioridad sobre variable de entorno
    for arg in sys.argv[1:]:
        if arg.startswith("PRIMITIVE="):
            value = arg.split("=")[1].lower()
            if value not in VALID_PRIMITIVES:
                raise ValueError(f"PRIMITIVE inválido: '{value}'. Usa: {VALID_PRIMITIVES}")
            return value
    # Fallback a variable de entorno
    env_value = os.getenv("PRIMITIVE", DEFAULT_PRIMITIVE).lower()
    if env_value not in VALID_PRIMITIVES:
        raise ValueError(f"PRIMITIVE inválido: '{env_value}'. Usa: {VALID_PRIMITIVES}")
    return env_value
