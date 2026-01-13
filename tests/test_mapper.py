"""Tests para mapper"""

"""
Tests para el módulo mapper.
"""
import pytest
from ontology2db.parser import Class, Attribute, Relation, Ontology
from ontology2db.mapper import OntologyMapper


def test_map_simple_class():
    """Test mapeo de clase simple."""
    cls = Class(id="1", name="Person")
    cls.attributes.append(Attribute("name", "string", "1"))
    cls.attributes.append(Attribute("age", "int", "0..1"))
    
    ontology = Ontology(classes=[cls])
    mapper = OntologyMapper()
    schema = mapper.map(ontology)
    
    assert len(schema.tables) == 1
    table = schema.tables[0]
    assert table.name == "Person"
    assert len(table.columns) == 3  # id + name + age


def test_map_one_to_many_relation():
    """Test mapeo de relación uno-a-muchos."""
    author = Class(id="1", name="Author")
    book = Class(id="2", name="Book")
    rel = Relation("writes", "Author", "Book",
                   source_cardinality="1",
                   target_cardinality="0..n")
    
    ontology = Ontology(classes=[author, book], relations=[rel])
    mapper = OntologyMapper()
    schema = mapper.map(ontology)
    
    # Buscar foreign key en tabla Book
    book_table = schema.get_table("Book")
    fk_columns = [col for col in book_table.columns 
                  if col.foreign_key is not None]
    
    assert len(fk_columns) == 1
    assert fk_columns[0].foreign_key == "Author.id"


def test_map_many_to_many_relation():
    """Test mapeo de relación many-to-many."""
    student = Class(id="1", name="Student")
    course = Class(id="2", name="Course")
    rel = Relation("enrolls", "Student", "Course",
                   source_cardinality="0..n",
                   target_cardinality="0..n")
    
    ontology = Ontology(classes=[student, course], relations=[rel])
    mapper = OntologyMapper()
    schema = mapper.map(ontology)
    
    # Debe haber 3 tablas: Student, Course y Student_Course
    assert len(schema.tables) == 3
    
    # Buscar tabla de asociación
    assoc_tables = [t for t in schema.tables if t.is_association_table]
    assert len(assoc_tables) == 1