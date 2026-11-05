import sys

DEFAULT_SHOTS = 100  # default interno seguro para hardware real


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
