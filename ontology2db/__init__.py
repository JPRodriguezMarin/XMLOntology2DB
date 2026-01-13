"""Ontology to Database Converter"""
__version__ = "1.0.0"

"""
Ontology to Database Converter
Convierte ontologías XML a modelos SQLAlchemy y esquemas relacionales.
"""

__version__ = "1.0.0"

from .parser import OntologyParser
from .mapper import OntologyMapper
from .codegen import SQLAlchemyGenerator
from .visualizer import OntologyVisualizer

__all__ = [
    "OntologyParser",
    "OntologyMapper", 
    "SQLAlchemyGenerator",
    "OntologyVisualizer"
]
