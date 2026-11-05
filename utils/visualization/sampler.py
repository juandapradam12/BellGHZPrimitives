"""
sampler.py
-----------
Funciones de visualización para resultados del Sampler primitive.
"""
import os
import matplotlib.pyplot as plt


def plot_sampler_results(counts: dict, n_shots: int, n_qubits: int,
                         top_n: int = 10, save_path: str = None):
    """
    Visualiza la distribución de bitstrings del Sampler:
    - Gráfico de barras con los `top_n` estados más frecuentes.
    - Para un estado GHZ ideal se esperan sólo |000...0⟩ y |111...1⟩.

    Args:
        counts    — dict {bitstring: count}
        n_shots   — número total de shots (para calcular probabilidades)
        n_qubits  — número de qubits del circuito
        top_n     — cuántos estados mostrar (por defecto 10)
        save_path — ruta donde guardar la figura (opcional)
    """
    sorted_counts = sorted(counts.items(), key=lambda x: -x[1])[:top_n]
    labels = [f"|{bs}⟩" for bs, _ in sorted_counts]
    probs  = [cnt / n_shots for _, cnt in sorted_counts]

    # Colorear en rojo los dos estados GHZ ideales, azul el resto
    ghz_zero = "0" * n_qubits
    ghz_one  = "1" * n_qubits
    colors = [
        "#E91E63" if bs in (ghz_zero, ghz_one) else "#2196F3"
        for bs, _ in sorted_counts
    ]

    fig, ax = plt.subplots(figsize=(max(8, len(labels) * 0.9), 5))
    bars = ax.bar(labels, probs, color=colors, edgecolor="black", linewidth=0.8)
    ax.set_xlabel("Estado de medición")
    ax.set_ylabel("Probabilidad")
    ax.set_title(
        f"Distribución Sampler — {n_qubits} qubits, {n_shots} shots\n"
        f"(rojo = estados GHZ ideales |{'0'*n_qubits}⟩ / |{'1'*n_qubits}⟩)"
    )
    ax.set_ylim(0, min(1.1, max(probs) * 1.25))
    ax.tick_params(axis="x", rotation=45)

    # Etiqueta de probabilidad encima de cada barra
    for bar, prob in zip(bars, probs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.005,
            f"{prob:.3f}",
            ha="center", va="bottom", fontsize=8
        )

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()
