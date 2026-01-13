"""Módulo codegen"""

"""
Generador de código SQLAlchemy.
"""
from typing import TextIO
from .mapper import RelationalSchema, Table, Column


class SQLAlchemyGenerator:
    """Genera código Python con modelos SQLAlchemy."""
    
    def generate(self, schema: RelationalSchema, output_file: str):
        """
        Genera código SQLAlchemy y lo escribe en un archivo.
        
        Args:
            schema: Esquema relacional
            output_file: Ruta del archivo de salida
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            self._write_header(f)
            self._write_base(f)
            
            for table in schema.tables:
                if table.is_association_table:
                    self._write_association_table(f, table)
                else:
                    self._write_model(f, table, schema)
            
            self._write_footer(f)
    
    def _write_header(self, f: TextIO):
        """Escribe el header del archivo."""
        f.write('"""\n')
        f.write('Modelos generados automáticamente desde ontología.\n')
        f.write('"""\n')
        f.write('from sqlalchemy import Column, Integer, String, Text, Float, '
                'Boolean, DateTime, Date, Time\n')
        f.write('from sqlalchemy import ForeignKey, Table, UniqueConstraint\n')
        f.write('from sqlalchemy.orm import declarative_base, relationship\n')
        f.write('from sqlalchemy import create_engine\n')
        f.write('from sqlalchemy.orm import Session\n\n')
    
    def _write_base(self, f: TextIO):
        """Escribe la definición de Base."""
        f.write('Base = declarative_base()\n\n')
    
    def _write_association_table(self, f: TextIO, table: Table):
        """Escribe una tabla de asociación."""
        f.write(f'\n# Tabla de asociación: {table.name}\n')
        f.write(f'{table.name} = Table(\n')
        f.write(f'    "{table.name}",\n')
        f.write('    Base.metadata,\n')
        
        for col in table.columns:
            f.write(f'    Column("{col.name}", {col.type}')
            if col.foreign_key:
                f.write(f', ForeignKey("{col.foreign_key}")')
            if col.primary_key:
                f.write(', primary_key=True')
            f.write('),\n')
        
        f.write(')\n\n')
    
    def _write_model(self, f: TextIO, table: Table, schema: RelationalSchema):
        """Escribe una clase modelo."""
        f.write(f'\nclass {table.name}(Base):\n')
        
        if table.description:
            f.write(f'    """{table.description}"""\n')
        
        f.write(f'    __tablename__ = "{table.name}"\n\n')
        
        # Escribir columnas
        for col in table.columns:
            f.write(f'    {col.name} = Column({col.type}')
            
            if col.primary_key:
                f.write(', primary_key=True')
            if col.foreign_key:
                f.write(f', ForeignKey("{col.foreign_key}")')
            if not col.nullable and not col.primary_key:
                f.write(', nullable=False')
            if col.unique:
                f.write(', unique=True')
            
            f.write(')\n')
        
        # Escribir relationships
        self._write_relationships(f, table, schema)
        
        f.write(f'\n    def __repr__(self):\n')
        f.write(f'        return f"<{table.name}(id={{self.id}})>"\n\n')
    
    def _write_relationships(self, f: TextIO, table: Table, 
                            schema: RelationalSchema):
        """Escribe las relaciones del modelo."""
        # Buscar foreign keys en esta tabla
        for col in table.columns:
            if col.foreign_key and not col.primary_key:
                ref_table = col.foreign_key.split('.')[0]
                rel_name = ref_table.lower()
                f.write(f'    {rel_name} = relationship("{ref_table}", '
                       f'back_populates="{table.name.lower()}s")\n')
        
        # Buscar referencias desde otras tablas
        for other_table in schema.tables:
            if other_table.name != table.name and not other_table.is_association_table:
                for col in other_table.columns:
                    if col.foreign_key == f"{table.name}.id":
                        f.write(f'    {other_table.name.lower()}s = relationship('
                               f'"{other_table.name}", '
                               f'back_populates="{table.name.lower()}")\n')
        
        # Buscar tablas de asociación
        for assoc_table in schema.tables:
            if assoc_table.is_association_table and table.name in assoc_table.name:
                parts = assoc_table.name.split('_')
                if parts[0] == table.name:
                    other = parts[1]
                    f.write(f'    {other.lower()}s = relationship('
                           f'"{other}", secondary="{assoc_table.name}", '
                           f'back_populates="{table.name.lower()}s")\n')
                elif parts[1] == table.name:
                    other = parts[0]
                    f.write(f'    {other.lower()}s = relationship('
                           f'"{other}", secondary="{assoc_table.name}", '
                           f'back_populates="{table.name.lower()}s")\n')
    
    def _write_footer(self, f: TextIO):
        """Escribe funciones auxiliares."""
        f.write('\n\ndef create_database(db_url: str = "sqlite:///ontology.db"):\n')
        f.write('    """Crea la base de datos con todas las tablas."""\n')
        f.write('    engine = create_engine(db_url, echo=True)\n')
        f.write('    Base.metadata.create_all(engine)\n')
        f.write('    return engine\n\n')
        f.write('def get_session(engine):\n')
        f.write('    """Retorna una sesión de SQLAlchemy."""\n')
        f.write('    return Session(engine)\n\n')
        f.write('def export_ddl(db_url: str = "sqlite:///ontology.db"):\n')
        f.write('    """Exporta el DDL SQL."""\n')
        f.write('    from sqlalchemy.schema import CreateTable\n')
        f.write('    engine = create_engine(db_url)\n')
        f.write('    for table in Base.metadata.sorted_tables:\n')
        f.write('        print(f"\\n-- Table: {table.name}")\n')
        f.write('        print(CreateTable(table).compile(engine))\n')
    def export_ddl_to_files(self, schema: RelationalSchema, output_dir: str):
        """
        Exporta cada tabla a un archivo .sql individual.
        
        Args:
            schema: Esquema relacional
            output_dir: Directorio base donde crear carpeta con timestamp
        """
        from datetime import datetime
        from pathlib import Path
        from sqlalchemy import create_engine, MetaData, Table as SQLATable, Column as SQLAColumn
        from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime as SQLADateTime, Date, Time
        from sqlalchemy import ForeignKey
        from sqlalchemy.schema import CreateTable
        
        # Crear carpeta con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = Path(output_dir) / timestamp
        export_path.mkdir(parents=True, exist_ok=True)
        
        # Motor temporal para compilar DDL
        engine = create_engine("sqlite:///:memory:")
        metadata = MetaData()
        
        # Mapeo de tipos
        type_map = {
            'Integer': Integer,
            'String': String,
            'Text': Text,
            'Float': Float,
            'Boolean': Boolean,
            'DateTime': SQLADateTime,
            'Date': Date,
            'Time': Time
        }
        
        # PASO 1: Crear todas las tablas en metadata primero (sin DDL todavía)
        sqla_tables = {}
        for table in schema.tables:
            columns = []
            for col in table.columns:
                col_type = type_map.get(col.type, String)
                col_args = []
                col_kwargs = {}
                
                if col.foreign_key:
                    # Agregar FK pero sin validar todavía
                    col_args.append(ForeignKey(col.foreign_key))
                
                if col.primary_key:
                    col_kwargs['primary_key'] = True
                if not col.nullable and not col.primary_key:
                    col_kwargs['nullable'] = False
                if col.unique:
                    col_kwargs['unique'] = True
                
                columns.append(SQLAColumn(col.name, col_type, *col_args, **col_kwargs))
            
            sqla_tables[table.name] = SQLATable(table.name, metadata, *columns)
        
        # PASO 2: Ordenar tablas por dependencias
        def get_table_order():
            """Ordena tablas para que las independientes vayan primero."""
            ordered = []
            processed = set()
            
            def has_unprocessed_deps(tbl):
                """Verifica si tiene dependencias no procesadas."""
                for col in tbl.columns:
                    if col.foreign_key:
                        ref_table = col.foreign_key.split('.')[0]
                        if ref_table not in processed and ref_table != tbl.name:
                            return True
                return False
            
            # Agregar tablas sin dependencias primero
            changed = True
            while changed and len(ordered) < len(schema.tables):
                changed = False
                for table in schema.tables:
                    if table.name not in processed:
                        if not has_unprocessed_deps(table):
                            ordered.append(table)
                            processed.add(table.name)
                            changed = True
            
            # Agregar las restantes (referencias circulares)
            for table in schema.tables:
                if table.name not in processed:
                    ordered.append(table)
            
            return ordered
        
        sorted_tables = get_table_order()
        
        # PASO 3: Generar DDL para cada tabla en orden
        for table in sorted_tables:
            sqla_table = sqla_tables[table.name]
            
            # Generar DDL
            ddl = str(CreateTable(sqla_table).compile(engine))
            
            # Guardar en archivo
            table_name = table.name.lower()
            sql_file = export_path / f"{table_name}.sql"
            sql_file.write_text(ddl, encoding='utf-8')
            print(f"     ✓ {table_name}.sql")
        
        return export_path