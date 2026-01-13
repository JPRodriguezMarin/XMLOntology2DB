"""Módulo parser"""

"""
Parser para ontologías en formato XML.
"""

import xml.etree.ElementTree as ET
import textwrap
import re
from typing import Optional
from dataclasses import dataclass, field
from typing import List


@dataclass
class Attribute:
    """Representa un atributo de una clase."""
    name: str
    type: str
    cardinality: str = "1"
    description: Optional[str] = None
    
    def is_required(self) -> bool:
        """Verifica si el atributo es obligatorio."""
        return self.cardinality in ["1", "1..1", "1..n"]
    
    def is_multiple(self) -> bool:
        """Verifica si el atributo permite múltiples valores."""
        return ".." in self.cardinality and self.cardinality.split("..")[-1] in ["n", "*"]


@dataclass
class Class:
    """Representa una clase de la ontología."""
    id: str
    name: str
    description: Optional[str] = None
    attributes: List[Attribute] = field(default_factory=list)


@dataclass
class Relation:
    """Representa una relación entre clases."""
    name: str
    source: str
    target: str
    type: str = "association"  # association, aggregation, composition
    source_cardinality: str = "1"
    target_cardinality: str = "1"
    description: Optional[str] = None
    properties: List[Attribute] = field(default_factory=list)
    
    def is_many_to_many(self) -> bool:
        """Verifica si es una relación muchos a muchos."""
        source_multiple = ".." in self.source_cardinality and \
                         self.source_cardinality.split("..")[-1] in ["n", "*"]
        target_multiple = ".." in self.target_cardinality and \
                         self.target_cardinality.split("..")[-1] in ["n", "*"]
        return source_multiple and target_multiple
    
    def is_one_to_many(self) -> bool:
        """Verifica si es una relación uno a muchos."""
        target_multiple = ".." in self.target_cardinality and \
                         self.target_cardinality.split("..")[-1] in ["n", "*"]
        source_single = self.source_cardinality in ["1", "0..1", "1..1"]
        return source_single and target_multiple


@dataclass
class Ontology:
    """Representa una ontología completa."""
    classes: List[Class] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)


class OntologyParser:
    """Parser de ontologías XML."""
    
    def parse(self, xml_file: str) -> Ontology:
        """
        Parsea un archivo XML y retorna un objeto Ontology.
        
        Args:
            xml_file: Ruta al archivo XML
            
        Returns:
            Objeto Ontology con clases y relaciones
        """
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        ontology = Ontology()
        
        # Parsear clases
        for class_elem in root.findall(".//Class"):
            cls = self._parse_class(class_elem)
            ontology.classes.append(cls)
        
        # Parsear relaciones
        for rel_elem in root.findall(".//Relation"):
            rel = self._parse_relation(rel_elem)
            ontology.relations.append(rel)
        
        return ontology
    
    def _clean_description(self, text: Optional[str]) -> Optional[str]:
        """
        Limpia la descripción preservando saltos de línea y
        eliminando indentación artificial del XML.
        """
        if not text:
            return None
        return textwrap.dedent(text).strip()
    
    def _parse_docstring_description(self, text: Optional[str]):
        """
        Separa descripción de clase y atributos a partir de docstring Sphinx.

        Retorna:
            class_description: str
            attr_descriptions: dict(nombre_atributo -> descripción)
        """
        if not text:
            return "", {}

        text = textwrap.dedent(text).strip()

        # Extraer descripciones de atributos
        attr_pattern = re.compile(
            r":param\s+(\w+)\s*:\s*(.+?)(?=\n\s*:param|\n\s*:type|\Z)",
            re.DOTALL
        )
        attr_descriptions = {
            name: desc.strip().replace("\n", " ")
            for name, desc in attr_pattern.findall(text)
        }

        # Descripción de clase = todo antes del primer :param
        class_desc = text.split(":param")[0]
        # Limpiar encabezados de docstring que no sean útiles
       
        class_desc = class_desc.strip()

        # Tomar solo la frase relevante si hay varias
        #if "." in class_desc:
         #   sentences = [s.strip() for s in class_desc.split(".") if s.strip()]
          #  if sentences:
           #     class_desc = sentences[0]

        return class_desc, attr_descriptions
    
    def _parse_class(self, elem: ET.Element) -> Class:
        raw_description = self._clean_description(elem.findtext("description"))
        class_desc, attr_descs = self._parse_docstring_description(raw_description)

        cls = Class(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            description=class_desc
        )

        # Parsear atributos
        for attr_elem in elem.findall(".//Attribute"):
            name = attr_elem.get("name", "")
            attr = Attribute(
                name=name,
                type=attr_elem.get("type", "string"),
                cardinality=attr_elem.get("cardinality", attr_elem.get("multiplicity", "1")),
                description=attr_descs.get(name, self._clean_description(attr_elem.findtext("description")))
            )
            cls.attributes.append(attr)

        return cls
    
    def _parse_relation(self, elem: ET.Element) -> Relation:
        """Parsea un elemento Relation."""
        rel = Relation(
            name=elem.get("name", ""),
            source=elem.get("source", ""),
            target=elem.get("target", ""),
            type=elem.get("type", "association"),
            source_cardinality=elem.get("source_cardinality", "1"),
            target_cardinality=elem.get("target_cardinality", "1"),
            description=self._clean_description(
                elem.findtext("description")
            )
        )
        
        # Parsear propiedades de la relación
        for prop_elem in elem.findall(".//Property"):
            prop = Attribute(
                name=prop_elem.get("name", ""),
                type=prop_elem.get("type", "string"),
                cardinality=prop_elem.get("cardinality", "1"),
                description=self._clean_description(
                    prop_elem.findtext("description")
                )
            )
            rel.properties.append(prop)
        
        return rel