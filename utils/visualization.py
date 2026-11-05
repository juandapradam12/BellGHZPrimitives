import os
import matplotlib.pyplot as plt
import numpy as np


def plot_estimator_results(observables_labels, evs, stds, save_path=None):
    """
    Visualiza los resultados del Estimator:
    - Gráfico de barras con barras de error
    - Heatmap de valores esperados (solo si n es factorizable en 2 filas)
    """
    n = len(evs)
    # Intentar reshape en 2 filas solo si es divisible
    can_heatmap = (n % 2 == 0)
    ncols_plot = 2 if can_heatmap else 1
    fig, axes = plt.subplots(1, ncols_plot, figsize=(7 * ncols_plot, 5))
    if ncols_plot == 1:
        axes = [axes]

    # 1. Gráfico de barras con barras de error
    colors = ["#2196F3" if abs(ev) < 0.5 else "#E91E63" for ev in evs]
    axes[0].bar(observables_labels, evs, yerr=stds, capsize=6,
                color=colors, edgecolor="black", linewidth=0.8)
    axes[0].axhline(0, color="black", linewidth=0.8, linestyle="--")
    axes[0].axhline(1, color="gray", linewidth=0.6, linestyle=":")
    axes[0].axhline(-1, color="gray", linewidth=0.6, linestyle=":")
    axes[0].set_ylim(-1.3, 1.3)
    axes[0].set_xlabel("Observable")
    axes[0].set_ylabel("Valor esperado ⟨O⟩")
    axes[0].set_title("Valores esperados\n(Estimator)")
    axes[0].tick_params(axis='x', rotation=45)

    # 2. Heatmap (solo si aplica)
    if can_heatmap:
        rows = 2
        cols = n // 2
        matrix = np.array(evs).reshape(rows, cols)
        labels_matrix = np.array(observables_labels).reshape(rows, cols)
        im = axes[1].imshow(matrix, cmap="RdBu", vmin=-1, vmax=1, aspect="auto")
        for i in range(rows):
            for j in range(cols):
                axes[1].text(j, i, f"{labels_matrix[i,j]}\n{matrix[i,j]:.3f}",
                             ha="center", va="center", fontsize=9, fontweight="bold")
        axes[1].set_xticks([])
        axes[1].set_yticks([])
        axes[1].set_title("Mapa de valores esperados\n(azul=negativo, rojo=positivo)")
        plt.colorbar(im, ax=axes[1], label="⟨O⟩")

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()


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


def plot_ghz_decay(evs, n_qubits: int, label: str = "GHZ state", save_path=None):
    """
    Visualiza el decaimiento de las correlaciones ZZ con la distancia entre qubits.
    Solo aplica para GHZ states (N_QUBITS > 2).
    """
    import matplotlib.pyplot as plt

    data = list(range(1, len(evs) + 1))
    values_normalized = [v / evs[0] for v in evs]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data, values_normalized, marker="o", label=f"{n_qubits}-qubit {label}")
    ax.set_xlabel("Distance between qubits $i$")
    ax.set_ylabel(r"$\langle Z_i Z_0 \rangle / \langle Z_1 Z_0 \rangle$")
    ax.legend()
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.show()
