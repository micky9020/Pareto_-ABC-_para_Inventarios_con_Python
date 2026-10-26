"""Gráficos del análisis de Pareto."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sin interfaz gráfica
import matplotlib.pyplot as plt
import pandas as pd

COLORES = {"A": "#c0392b", "B": "#f39c12", "C": "#2980b9"}


def grafico_pareto(df: pd.DataFrame, ruta_salida: str | Path, limite_a=0.80, limite_b=0.95) -> Path:
    """Diagrama de Pareto: barras de valor por SKU + curva de % acumulado."""
    fig, ax1 = plt.subplots(figsize=(13, 6))
    x = range(len(df))

    ax1.bar(x, df["valor_anual"], color=[COLORES[c] for c in df["clase"]], width=1.0)
    ax1.set_xlabel("SKUs ordenados por valor anual (mayor a menor)")
    ax1.set_ylabel("Valor anual de consumo")
    ax1.set_xticks([])
    ax1.set_xlim(-0.5, len(df) - 0.5)

    ax2 = ax1.twinx()
    ax2.plot(x, df["pct_acumulado"] * 100, color="black", linewidth=2)
    ax2.axhline(limite_a * 100, color=COLORES["A"], linestyle="--", linewidth=1)
    ax2.axhline(limite_b * 100, color=COLORES["B"], linestyle="--", linewidth=1)
    ax2.set_ylabel("% acumulado del valor")
    ax2.set_ylim(0, 105)

    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORES[c]) for c in "ABC"]
    ax1.legend(handles, ["Clase A", "Clase B", "Clase C"], loc="center right")
    plt.title("Análisis de Pareto (ABC) del inventario")
    fig.tight_layout()

    ruta = Path(ruta_salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def grafico_distribucion_abc(resumen: pd.DataFrame, ruta_salida: str | Path) -> Path:
    """Compara el % de SKUs vs. el % de valor de cada clase."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ancho = 0.38
    pos = range(len(resumen))

    b1 = ax.bar([p - ancho / 2 for p in pos], resumen["pct_skus"] * 100, ancho, label="% de SKUs", color="#7f8c8d")
    b2 = ax.bar([p + ancho / 2 for p in pos], resumen["pct_valor"] * 100, ancho, label="% del valor", color="#16a085")
    for barras in (b1, b2):
        ax.bar_label(barras, fmt="%.1f%%", padding=2)

    ax.set_xticks(list(pos))
    ax.set_xticklabels([f"Clase {c}" for c in resumen["clase"]])
    ax.set_ylabel("Porcentaje")
    ax.set_ylim(0, 105)
    ax.legend()
    plt.title("Distribución ABC: SKUs vs. valor")
    fig.tight_layout()

    ruta = Path(ruta_salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta
