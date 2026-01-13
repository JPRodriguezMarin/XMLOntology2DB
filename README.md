# Ontology2DB - Conversor de Ontologías XML a SQLAlchemy

Sistema completo para convertir ontologías XML en modelos SQLAlchemy, esquemas relacionales y visualizaciones de grafo.

## 🚀 Características

- ✅ **Parsing robusto de XML** con soporte para clases, atributos y relaciones
- ✅ **Mapeo automático** a esquemas relacionales
- ✅ **Generación de código SQLAlchemy** con modelos declarativos
- ✅ **Manejo inteligente de cardinalidades**: 1:1, 1:N, N:M
- ✅ **Visualización interactiva** con pyvis (HTML) y matplotlib (PNG)
- ✅ **Exportación de DDL SQL** para documentación
- ✅ **CLI fácil de usar** para automatización
- ✅ **Tests unitarios** con pytest

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/ontology2db.git
cd ontology2db

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar en modo desarrollo
pip install -e .
```

## 🎯 Uso Rápido

### Desde línea de comandos:

```bash
# Convertir ontología y generar modelos
ontology2db examples/example_ontology.xml -o models.py

# Con visualización interactiva
ontology2db examples/example_ontology.xml -o models.py -v pyvis

# Solo visualización, sin generar modelos
ontology2db examples/example_ontology.xml -v both --no-models
```

### Desde Python:

```python
from ontology2db import (
    OntologyParser,
    OntologyMapper,
    SQLAlchemyGenerator,
    OntologyVisualizer
)

# 1. Parsear XML
parser = OntologyParser()
ontology = parser.parse("mi_ontologia.xml")

# 2. Mapear a esquema relacional
mapper = OntologyMapper()
schema = mapper.map(ontology)

# 3. Generar código SQLAlchemy
generator = SQLAlchemyGenerator()
generator.generate(schema, "models.py")

# 4. Visualizar
visualizer = OntologyVisualizer(ontology)
visualizer.save_pyvis("graph.html")
```

## 📋 Formato XML Soportado

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Ontology>
    <!-- Clase con atributos -->
    <Class id="1" name="Author">
        <description>Representa un autor</description>
        <Attribute name="name" type="string" cardinality="1"/>
        <Attribute name="birth_date" type="date" cardinality="0..1"/>
    </Class>
    
    <Class id="2" name="Book">
        <Attribute name="title" type="string" cardinality="1"/>
        <Attribute name="isbn" type="string" cardinality="1"/>
    </Class>
    
    <!-- Relación uno-a-muchos -->
    <Relation name="writes" source="Author" target="Book" 
              type="association"
              source_cardinality="1" 
              target_cardinality="0..n"/>
    
    <!-- Relación muchos-a-muchos -->
    <Relation name="categorized" source="Book" target="Category"
              source_cardinality="0..n"
              target_cardinality="0..n">
        <Property name="assigned_date" type="datetime" cardinality="1"/>
    </Relation>
</Ontology>
```

## 🔧 Mapeo de Tipos

| Tipo XML | Tipo SQLAlchemy | SQL |
|----------|-----------------|-----|
| string   | String          | VARCHAR |
| text     | Text            | TEXT |
| int      | Integer         | INTEGER |
| float    | Float           | FLOAT |
| bool     | Boolean         | BOOLEAN |
| date     | Date            | DATE |
| datetime | DateTime        | DATETIME |

## 📊 Mapeo de Cardinalidades

| Cardinalidad | Comportamiento |
|--------------|----------------|
| `1`, `1..1`  | NOT NULL, relación obligatoria |
| `0..1`       | NULLABLE, relación opcional |
| `1..n`       | Foreign key + NOT NULL |
| `0..n`       | Foreign key + NULLABLE |
| `n..m`, `*`  | Tabla intermedia (many-to-many) |

## 🧪 Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=ontology2db --cov-report=html

# Tests específicos
pytest tests/test_parser.py
```

## 📖 Ejemplo Completo

Ejecuta el ejemplo incluido:

```bash
cd examples
python example.py
```

Esto generará:
- `generated_models.py` - Modelos SQLAlchemy
- `example.db` - Base de datos SQLite
- `ontology_graph.html` - Visualización interactiva
- `ontology_graph.png` - Visualización estática

## 🏗️ Estructura del Proyecto

```
ontology2db/
├── ontology2db/          # Código fuente
│   ├── __init__.py
│   ├── parser.py         # Parser XML
│   ├── mapper.py         # Mapeo ontología → relacional
│   ├── codegen.py        # Generador de código SQLAlchemy
│   ├── visualizer.py     # Visualización de grafos
│   └── cli.py            # Interfaz de línea de comandos
├── tests/                # Tests unitarios
│   ├── test_parser.py
│   ├── test_mapper.py
│   └── test_codegen.py
├── examples/             # Ejemplos de uso
│   ├── example_ontology.xml
│   └── example.py
├── requirements.txt      # Dependencias
├── setup.py             # Configuración del paquete
└── README.md            # Este archivo
```

## 🔍 Características Avanzadas

### Relaciones con Propiedades

Las relaciones pueden tener atributos propios que se convierten en columnas de la tabla intermedia:

```xml
<Relation name="enrollment" source="Student" target="Course"
          source_cardinality="0..n" target_cardinality="0..n">
    <Property name="enrollment_date" type="datetime" cardinality="1"/>
    <Property name="grade" type="float" cardinality="0..1"/>
</Relation>
```

### Exportar DDL SQL

```python
from generated_models import export_ddl
export_ddl()  # Imprime el DDL completo
```

### Usar los Modelos Generados

```python
from generated_models import Author, Book, create_database, get_session

# Crear BD
engine = create_database()
session = get_session(engine)

# Insertar datos
author = Author(name="Gabriel García Márquez", nationality="Colombia")
book = Book(title="Cien años de soledad", isbn="978-0060883287")
book.author = author

session.add(author)
session.add(book)
session.commit()

# Consultar
authors = session.query(Author).all()
for author in authors:
    print(f"{author.name} escribió {len(author.books)} libros")
```

## 🐛 Solución de Problemas

**Error: "pyvis not installed"**
```bash
pip install pyvis
```

**Error: "matplotlib not installed"**
```bash
pip install matplotlib
```

**Los grafos se ven mal**
- Ajusta los parámetros de layout en `visualizer.py`
- Prueba diferentes valores de `k` en `spring_layout`

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## ✨ Roadmap

- [ ] Soporte para herencia de clases
- [ ] Generación de migrations con Alembic
- [ ] Exportación a otros formatos (JSON, GraphML)
- [ ] GUI web con Flask/FastAPI
- [ ] Soporte para constraints personalizados
- [ ] Generación de documentación automática

