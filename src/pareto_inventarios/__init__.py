"""Análisis de Pareto (ABC) para bases de datos de inventarios."""

from .analisis import cargar_datos, clasificar_pareto, resumen_por_clase
from .graficos import grafico_pareto, grafico_distribucion_abc

__version__ = "1.0.0"
__all__ = [
    "cargar_datos",
    "clasificar_pareto",
    "resumen_por_clase",
    "grafico_pareto",
    "grafico_distribucion_abc",
]
