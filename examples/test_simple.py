"""
Script simple para probar solo el visualizador.
Ejecutar desde examples/: python test_simple.py
"""
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ontology2db import OntologyParser, OntologyVisualizer

print("="*70)
print("  PRUEBA SIMPLE DEL VISUALIZADOR")
print("="*70)

# 1. Parsear XML
print("\n1. Parseando XML...")
parser = OntologyParser()
ontology = parser.parse('example_ontology.xml')
print(f"   ✓ {len(ontology.classes)} clases, {len(ontology.relations)} relaciones")

# 2. Crear visualizador
print("\n2. Creando visualizador...")
viz = OntologyVisualizer(ontology)
print("   ✓ Grafo creado")

# 3. Verificar datos del grafo
print("\n3. Verificando datos...")

# Ver primer nodo
for node, data in viz.graph.nodes(data=True):
    print(f"\n   NODO: {node}")
    print(f"     - Label: {data.get('label')}")
    print(f"     - Title (tooltip):")
    title = data.get('title', '')
    if '<b>' in title and 'Atributos' in title:
        print("       ✓ Tiene tooltip HTML con atributos")
    else:
        print("       ✗ NO tiene tooltip correcto")
    break

# Ver primera relación
for source, target, data in viz.graph.edges(data=True):
    print(f"\n   RELACIÓN: {source} -> {target}")
    label = data.get('label', '')
    print(f"     - Label: {label}")
    
    # Verificar formato correcto
    if '[' in label and ']' in label and '  ' in label:
        print("       ✓ Formato correcto: [card] nombre [card]")
    else:
        print("       ✗ Formato incorrecto")
    
    if '\\n' in label:
        print("       ✗ ERROR: Contiene \\n visible")
    else:
        print("       ✓ Sin saltos de línea escapados")
    break

# 4. Generar HTML
print("\n4. Generando HTML...")
try:
    viz.save_pyvis('test_ontology_graph.html')
    print("   ✓ HTML generado: test_ontology_graph.html")
    
    # Verificar que el archivo existe
    if os.path.exists('test_ontology_graph.html'):
        size = os.path.getsize('test_ontology_graph.html')
        print(f"   ✓ Tamaño: {size:,} bytes")
        
        # Leer parte del contenido para verificar
        with open('test_ontology_graph.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if '"title":' in content and '<b>' in content:
                print("   ✓ Contiene tooltips HTML")
            else:
                print("   ✗ NO contiene tooltips")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# 5. Estadísticas
print("\n5. Estadísticas:")
viz.print_statistics()

print("\n" + "="*70)
print("SIGUIENTE PASO:")
print("  1. Cierra COMPLETAMENTE tu navegador")
print("  2. Abre: test_ontology_graph.html")
print("  3. Verifica que los nodos solo muestran nombres")
print("  4. Pasa el mouse sobre un nodo para ver atributos")
print("  5. Verifica que las relaciones se ven como: [1]  writes  [0..*]")
print("="*70)