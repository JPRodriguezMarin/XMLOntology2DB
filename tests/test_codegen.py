"""Tests para codegen"""

"""
Tests para el módulo codegen.
"""
import pytest
import tempfile
from ontology2db.mapper import RelationalSchema, Table, Column
from ontology2db.codegen import SQLAlchemyGenerator


def test_generate_simple_model():
    """Test generación de modelo simple."""
    schema = RelationalSchema()
    table = Table(name="Person")
    table.columns.append(Column("id", "Integer", nullable=False, primary_key=True))
    table.columns.append(Column("name", "String", nullable=False))
    schema.tables.append(table)
    
    generator = SQLAlchemyGenerator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        temp_path = f.name
    
    generator.generate(schema, temp_path)
    
    # Verificar que el archivo fue creado y contiene código válido
    with open(temp_path, 'r') as f:
        content = f.read()
        assert "class Person(Base)" in content
        assert "id = Column(Integer" in content
        assert "name = Column(String" in content
    
    import os
    os.unlink(temp_path)


# examples/example_ontology.xml
"""
<?xml version="1.0" encoding="UTF-8"?>
<Ontology>
    <Class id="1" name="Author">
        <description>Representa un autor de libros</description>
        <Attribute name="name" type="string" cardinality="1">
            <description>Nombre completo del autor</description>
        </Attribute>
        <Attribute name="birth_date" type="date" cardinality="0..1">
            <description>Fecha de nacimiento</description>
        </Attribute>
        <Attribute name="nationality" type="string" cardinality="0..1"/>
    </Class>
    
    <Class id="2" name="Book">
        <description>Representa un libro</description>
        <Attribute name="title" type="string" cardinality="1"/>
        <Attribute name="isbn" type="string" cardinality="1"/>
        <Attribute name="publication_year" type="int" cardinality="0..1"/>
        <Attribute name="pages" type="int" cardinality="0..1"/>
    </Class>
    
    <Class id="3" name="Publisher">
        <description>Editorial que publica libros</description>
        <Attribute name="name" type="string" cardinality="1"/>
        <Attribute name="country" type="string" cardinality="0..1"/>
        <Attribute name="founded_year" type="int" cardinality="0..1"/>
    </Class>
    
    <Class id="4" name="Review">
        <description>Reseña de un libro</description>
        <Attribute name="rating" type="int" cardinality="1"/>
        <Attribute name="comment" type="text" cardinality="0..1"/>
        <Attribute name="review_date" type="datetime" cardinality="1"/>
    </Class>
    
    <Class id="5" name="Category">
        <description>Categoría o género literario</description>
        <Attribute name="name" type="string" cardinality="1"/>
        <Attribute name="description" type="text" cardinality="0..1"/>
    </Class>
    
    <!-- Relación uno-a-muchos: Un autor escribe muchos libros -->
    <Relation name="writes" source="Author" target="Book" 
              type="association"
              source_cardinality="1" 
              target_cardinality="0..n">
        <description>Un autor puede escribir múltiples libros</description>
    </Relation>
    
    <!-- Relación uno-a-muchos: Una editorial publica muchos libros -->
    <Relation name="publishes" source="Publisher" target="Book"
              type="association"
              source_cardinality="1"
              target_cardinality="0..n">
        <description>Una editorial publica múltiples libros</description>
    </Relation>
    
    <!-- Relación uno-a-muchos: Un libro tiene muchas reseñas -->
    <Relation name="has_reviews" source="Book" target="Review"
              type="composition"
              source_cardinality="1"
              target_cardinality="0..n">
        <description>Un libro puede tener múltiples reseñas</description>
    </Relation>
    
    <!-- Relación muchos-a-muchos: Libros pertenecen a múltiples categorías -->
    <Relation name="belongs_to" source="Book" target="Category"
              type="association"
              source_cardinality="0..n"
              target_cardinality="0..n">
        <description>Un libro puede pertenecer a múltiples categorías</description>
    </Relation>
</Ontology>
"""