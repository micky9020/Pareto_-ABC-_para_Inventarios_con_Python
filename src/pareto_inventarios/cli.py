"""Interfaz de línea de comandos."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .analisis import cargar_datos, clasificar_pareto, resumen_por_clase
from .graficos import grafico_distribucion_abc, grafico_pareto


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Análisis de Pareto (ABC) de inventarios")
    p.add_argument("-i", "--input", default="data/inventario_ejemplo.csv", help="CSV/Excel de entrada")
    p.add_argument("-o", "--output", default="output", help="Carpeta de resultados")
    p.add_argument("--limite-a", type=float, default=0.80, help="Corte clase A (default 0.80)")
    p.add_argument("--limite-b", type=float, default=0.95, help="Corte clase B (default 0.95)")
    args = p.parse_args(argv)

    salida = Path(args.output)
    salida.mkdir(parents=True, exist_ok=True)

    df = cargar_datos(args.input)
    clasificado = clasificar_pareto(df, args.limite_a, args.limite_b)
    resumen = resumen_por_clase(clasificado)

    clasificado.to_csv(salida / "clasificacion_abc.csv", index=False)
    with pd.ExcelWriter(salida / "reporte_pareto.xlsx") as xl:
        resumen.to_excel(xl, sheet_name="Resumen", index=False)
        clasificado.to_excel(xl, sheet_name="Detalle", index=False)

    grafico_pareto(clasificado, salida / "pareto.png", args.limite_a, args.limite_b)
    grafico_distribucion_abc(resumen, salida / "distribucion_abc.png")

    print(f"SKUs analizados: {len(clasificado):,}")
    print(f"Valor anual total: {clasificado['valor_anual'].sum():,.2f}\n")
    mostrar = resumen.copy()
    mostrar["pct_skus"] = (mostrar["pct_skus"] * 100).round(1).astype(str) + "%"
    mostrar["pct_valor"] = (mostrar["pct_valor"] * 100).round(1).astype(str) + "%"
    mostrar["valor_anual"] = mostrar["valor_anual"].map("{:,.2f}".format)
    print(mostrar.to_string(index=False))
    print(f"\nResultados guardados en: {salida.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
