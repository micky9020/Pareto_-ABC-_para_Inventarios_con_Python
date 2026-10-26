"""Punto de entrada: python main.py -i data/inventario_ejemplo.csv"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from pareto_inventarios.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
