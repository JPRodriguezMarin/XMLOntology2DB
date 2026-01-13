"""Módulo mapper"""

"""
Mapper que convierte ontologías a esquemas relacionales.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .parser import Ontology, Class, Relation, Attribute


@dataclass
class Column:
    """Representa una columna en una tabla."""
    name: str
    type: str
    nullable: bool = True
    primary_key: bool = False
    foreign_key: Optional[str] = None
    unique: bool = False


@dataclass
class Table:
    """Representa una tabla en el esquema relacional."""
    name: str
    columns: List[Column] = field(default_factory=list)
    is_association_table: bool = False
    description: Optional[str] = None


@dataclass
class RelationalSchema:
    """Esquema relacional completo."""
    tables: List[Table] = field(default_factory=list)
    
    def get_table(self, name: str) -> Optional[Table]:
        """Obtiene una tabla por nombre."""
        for table in self.tables:
            if table.name == name:
                return table
        return None


class OntologyMapper:
    """Mapea ontologías a esquemas relacionales."""
    
    TYPE_MAPPING = {
        "string": "String",
        "text": "Text",
        "int": "Integer",
        "integer": "Integer",
        "float": "Float",
        "double": "Float",
        "bool": "Boolean",
        "boolean": "Boolean",
        "datetime": "DateTime",
        "date": "Date",
        "time": "Time"
    }
    
    def map(self, ontology: Ontology) -> RelationalSchema:
        """
        Convierte una ontología a un esquema relacional.
        
        Args:
            ontology: Objeto Ontology a convertir
            
        Returns:
            RelationalSchema con tablas y columnas
        """
        schema = RelationalSchema()
        
        # Mapear clases a tablas
        for cls in ontology.classes:
            table = self._map_class_to_table(cls)
            schema.tables.append(table)
        
        # Mapear relaciones
        for rel in ontology.relations:
            self._map_relation(rel, schema, ontology)
        
        return schema
    
    def _map_class_to_table(self, cls: Class) -> Table:
        """Convierte una clase a una tabla."""
        table = Table(
            name=cls.name,
            description=cls.description
        )
        
        # Agregar primary key
        table.columns.append(Column(
            name="id",
            type="Integer",
            nullable=False,
            primary_key=True
        ))
        
        # Mapear atributos a columnas
        for attr in cls.attributes:
            if not attr.is_multiple():  # Solo atributos simples
                column = Column(
                    name=attr.name,
                    type=self._map_type(attr.type),
                    nullable=not attr.is_required()
                )
                table.columns.append(column)
        
        return table
    
    def _map_relation(self, rel: Relation, schema: RelationalSchema, 
                     ontology: Ontology):
        """Mapea una relación al esquema."""
        if rel.is_many_to_many():
            # Crear tabla intermedia
            self._create_association_table(rel, schema)
        elif rel.is_one_to_many():
            # Agregar foreign key a la tabla "muchos"
            self._add_foreign_key(rel, schema)
        else:
            # Relación uno a uno
            self._add_foreign_key(rel, schema, unique=True)
    
    def _create_association_table(self, rel: Relation, schema: RelationalSchema):
        """Crea una tabla de asociación para relaciones many-to-many."""
        table_name = f"{rel.source}_{rel.target}"
        
        table = Table(
            name=table_name,
            is_association_table=True,
            description=rel.description
        )
        
        # Columnas de foreign keys
        table.columns.append(Column(
            name=f"{rel.source.lower()}_id",
            type="Integer",
            nullable=False,
            foreign_key=f"{rel.source}.id",
            primary_key=True
        ))
        
        table.columns.append(Column(
            name=f"{rel.target.lower()}_id",
            type="Integer",
            nullable=False,
            foreign_key=f"{rel.target}.id",
            primary_key=True
        ))
        
        # Agregar propiedades de la relación
        for prop in rel.properties:
            table.columns.append(Column(
                name=prop.name,
                type=self._map_type(prop.type),
                nullable=not prop.is_required()
            ))
        
        schema.tables.append(table)
    
    def _add_foreign_key(self, rel: Relation, schema: RelationalSchema, 
                        unique: bool = False):
        """Agrega una foreign key a la tabla target."""
        target_table = schema.get_table(rel.target)
        if target_table:
            fk_column = Column(
                name=f"{rel.source.lower()}_id",
                type="Integer",
                nullable="0" in rel.source_cardinality,
                foreign_key=f"{rel.source}.id",
                unique=unique
            )
            target_table.columns.append(fk_column)
    
    def _map_type(self, type_str: str) -> str:
        """Mapea tipos de la ontología a tipos SQLAlchemy."""
        return self.TYPE_MAPPING.get(type_str.lower(), "String")