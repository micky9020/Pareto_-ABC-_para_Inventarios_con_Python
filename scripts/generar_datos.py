"""Genera un inventario sintético con distribución tipo Pareto."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

CATEGORIAS = ["Electrónica", "Ferretería", "Papelería", "Limpieza", "Empaque", "Repuestos"]


def generar(n: int = 500, semilla: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    # Lognormal => pocos SKUs concentran la mayor parte del valor
    demanda = rng.lognormal(mean=5.0, sigma=1.2, size=n).round().clip(min=1)
    costo = rng.lognormal(mean=2.5, sigma=1.3, size=n).round(2).clip(min=0.1)
    return pd.DataFrame(
        {
            "sku": [f"SKU-{i:04d}" for i in range(1, n + 1)],
            "descripcion": [f"Artículo {i}" for i in range(1, n + 1)],
            "categoria": rng.choice(CATEGORIAS, size=n),
            "demanda_anual": demanda.astype(int),
            "costo_unitario": costo,
            "stock_actual": rng.integers(0, 2000, size=n),
        }
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=500)
    ap.add_argument("-o", default="data/inventario_ejemplo.csv")
    a = ap.parse_args()
    Path(a.o).parent.mkdir(parents=True, exist_ok=True)
    generar(a.n).to_csv(a.o, index=False)
    print(f"Generado {a.o} con {a.n} SKUs")
