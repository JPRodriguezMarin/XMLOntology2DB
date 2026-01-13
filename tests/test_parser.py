"""Tests para parser"""

"""
Tests para el módulo parser.
"""
import pytest
import xml.etree.ElementTree as ET
from io import StringIO
from ontology2db.parser import OntologyParser, Class, Attribute, Relation


def test_parse_simple_class():
    """Test parsing de una clase simple."""
    xml_content = """<?xml version="1.0"?>
    <Ontology>
        <Class id="1" name="Person">
            <description>Una persona</description>
            <Attribute name="name" type="string" cardinality="1"/>
            <Attribute name="age" type="int" cardinality="0..1"/>
        </Class>
    </Ontology>
    """
    
    # Crear archivo temporal
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(xml_content)
        temp_path = f.name
    
    parser = OntologyParser()
    ontology = parser.parse(temp_path)
    
    assert len(ontology.classes) == 1
    assert ontology.classes[0].name == "Person"
    assert len(ontology.classes[0].attributes) == 2
    
    import os
    os.unlink(temp_path)


def test_parse_relation():
    """Test parsing de relaciones."""
    xml_content = """<?xml version="1.0"?>
    <Ontology>
        <Class id="1" name="Author"/>
        <Class id="2" name="Book"/>
        <Relation name="writes" source="Author" target="Book" 
                  type="association" 
                  source_cardinality="1" 
                  target_cardinality="0..n"/>
    </Ontology>
    """
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(xml_content)
        temp_path = f.name
    
    parser = OntologyParser()
    ontology = parser.parse(temp_path)
    
    assert len(ontology.relations) == 1
    assert ontology.relations[0].name == "writes"
    assert ontology.relations[0].source == "Author"
    
    import os
    os.unlink(temp_path)


def test_attribute_is_required():
    """Test verificación de atributos requeridos."""
    attr1 = Attribute("name", "string", "1")
    attr2 = Attribute("email", "string", "0..1")
    
    assert attr1.is_required() == True
    assert attr2.is_required() == False


def test_relation_is_many_to_many():
    """Test detección de relaciones many-to-many."""
    rel = Relation("enrolls", "Student", "Course",
                   source_cardinality="0..n",
                   target_cardinality="0..n")
    
    assert rel.is_many_to_many() == True