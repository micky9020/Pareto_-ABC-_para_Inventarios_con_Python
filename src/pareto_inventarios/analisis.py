"""Lógica del análisis de Pareto / clasificación ABC de inventarios."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

COLUMNAS_REQUERIDAS = ["sku", "descripcion", "demanda_anual", "costo_unitario"]


def cargar_datos(ruta: str | Path) -> pd.DataFrame:
    """Carga un CSV o Excel de inventario y valida sus columnas.

    El archivo debe contener: sku, descripcion, demanda_anual, costo_unitario.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    if ruta.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(ruta)
    else:
        df = pd.read_csv(ruta)

    df.columns = [c.strip().lower() for c in df.columns]
    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    if faltantes:
        raise ValueError(
            f"Faltan columnas requeridas: {faltantes}. "
            f"Columnas encontradas: {list(df.columns)}"
        )

    for col in ("demanda_anual", "costo_unitario"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["demanda_anual", "costo_unitario"])
    df = df[(df["demanda_anual"] >= 0) & (df["costo_unitario"] >= 0)]
    return df.reset_index(drop=True)


def clasificar_pareto(
    df: pd.DataFrame,
    limite_a: float = 0.80,
    limite_b: float = 0.95,
) -> pd.DataFrame:
    """Calcula el valor anual, el % acumulado y la clase ABC de cada SKU.

    Clase A: hasta ``limite_a`` del valor acumulado (por defecto 80 %).
    Clase B: hasta ``limite_b`` (por defecto 95 %).
    Clase C: el resto.
    """
    if not 0 < limite_a < limite_b <= 1:
        raise ValueError("Se requiere 0 < limite_a < limite_b <= 1")

    res = df.copy()
    res["valor_anual"] = res["demanda_anual"] * res["costo_unitario"]
    res = res.sort_values("valor_anual", ascending=False).reset_index(drop=True)

    total = res["valor_anual"].sum()
    if total <= 0:
        raise ValueError("El valor total del inventario es cero; no hay nada que analizar.")

    res["pct_valor"] = res["valor_anual"] / total
    res["pct_acumulado"] = res["pct_valor"].cumsum()
    res["pct_skus_acumulado"] = (res.index + 1) / len(res)

    # Un SKU entra en una clase si el acumulado ANTES de sumarlo aún no alcanzaba el límite.
    acumulado_previo = res["pct_acumulado"] - res["pct_valor"]
    res["clase"] = "C"
    res.loc[acumulado_previo < limite_b - 1e-9, "clase"] = "B"
    res.loc[acumulado_previo < limite_a - 1e-9, "clase"] = "A"
    return res


def resumen_por_clase(df_clasificado: pd.DataFrame) -> pd.DataFrame:
    """Resume cantidad de SKUs y valor por clase A/B/C."""
    n_total = len(df_clasificado)
    resumen = (
        df_clasificado.groupby("clase")
        .agg(n_skus=("sku", "count"), valor_anual=("valor_anual", "sum"))
        .reindex(["A", "B", "C"])
        .fillna(0)
    )
    resumen["pct_skus"] = resumen["n_skus"] / n_total
    resumen["pct_valor"] = resumen["valor_anual"] / resumen["valor_anual"].sum()
    return resumen.reset_index()
