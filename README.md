# Ontology2DB

Conversor de ontologías XML a modelos SQLAlchemy.

## Instalación

```bash
cd ontology2db
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Uso

```bash
ontology2db examples/example_ontology.xml -o models.py -v pyvis
```

## Tests

```bash
pytest tests/
```

Ver documentación completa en los artifacts.
