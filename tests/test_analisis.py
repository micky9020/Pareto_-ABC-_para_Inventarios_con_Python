import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pareto_inventarios import clasificar_pareto, resumen_por_clase  # noqa: E402


def _df():
    # Valores: 800, 100, 50, 30, 20  (total 1000)
    return pd.DataFrame(
        {
            "sku": list("ABCDE"),
            "descripcion": list("abcde"),
            "demanda_anual": [80, 10, 5, 3, 2],
            "costo_unitario": [10, 10, 10, 10, 10],
        }
    )


class TestPareto(unittest.TestCase):
    def test_orden_y_acumulado(self):
        r = clasificar_pareto(_df())
        self.assertEqual(r["sku"].tolist(), list("ABCDE"))
        self.assertAlmostEqual(r["pct_acumulado"].iloc[-1], 1.0)

    def test_clases(self):
        r = clasificar_pareto(_df())
        # Acumulados: 80%, 90%, 95%, 98%, 100%
        # A: 1 SKU (llega a 80%); B: hasta 95%; C: el resto
        self.assertEqual(r["clase"].tolist(), ["A", "B", "B", "C", "C"])

    def test_resumen_suma_100(self):
        s = resumen_por_clase(clasificar_pareto(_df()))
        self.assertAlmostEqual(s["pct_valor"].sum(), 1.0)
        self.assertEqual(s["n_skus"].sum(), 5)

    def test_limites_invalidos(self):
        with self.assertRaises(ValueError):
            clasificar_pareto(_df(), 0.9, 0.8)


if __name__ == "__main__":
    unittest.main()
