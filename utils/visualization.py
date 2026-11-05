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
