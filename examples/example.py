"""
Ejemplo de uso del conversor de ontologías.
"""
import os
import sys

# Asegurarse de que el módulo está en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ontology2db import (
    OntologyParser,
    OntologyMapper,
    SQLAlchemyGenerator,
    OntologyVisualizer
)


def main():
    print("=== Conversor de Ontologías XML a SQLAlchemy ===\n")
    
    # Determinar la ruta correcta del XML
    # Si estamos en examples/, usar ruta relativa simple
    # Si estamos en raíz, usar examples/CyberDEM_Ontology.xml
    if os.path.basename(os.getcwd()) == 'examples':
        xml_path = "CyberDEM_Ontology.xml"
        output_models = "generated_models.py"
        db_path = "sqlite:///example.db"  # Formato SQLAlchemy
    else:
        xml_path = "examples/CyberDEM_Ontology.xml"
        output_models = "examples/generated_models.py"
        db_path = "sqlite:///examples/example.db"  # Formato SQLAlchemy
    
    # Verificar que el archivo existe
    if not os.path.exists(xml_path):
        print(f"❌ Error: No se encuentra el archivo {xml_path}")
        print(f"   Directorio actual: {os.getcwd()}")
        print(f"   Archivos en directorio: {os.listdir('.')}")
        sys.exit(1)
    
    # 1. Parsear la ontología
    print("1. Parseando ontología desde XML...")
    parser = OntologyParser()
    ontology = parser.parse(xml_path)
    
    print(f"   ✓ Clases encontradas: {len(ontology.classes)}")
    for cls in ontology.classes:
        print(f"     - {cls.name} ({len(cls.attributes)} atributos)")
    
    print(f"   ✓ Relaciones encontradas: {len(ontology.relations)}")
    for rel in ontology.relations:
        print(f"     - {rel.source} --[{rel.name}]--> {rel.target}")
    
    # 2. Mapear a esquema relacional
    print("\n2. Mapeando a esquema relacional...")
    mapper = OntologyMapper()
    schema = mapper.map(ontology)
    
    print(f"   ✓ Tablas generadas: {len(schema.tables)}")
    for table in schema.tables:
        table_type = "asociación" if table.is_association_table else "entidad"
        print(f"     - {table.name} ({len(table.columns)} columnas, {table_type})")
    
    # 3. Generar código SQLAlchemy
    print("\n3. Generando código SQLAlchemy...")
    generator = SQLAlchemyGenerator()
    generator.generate(schema, output_models)
    print(f"   ✓ Código generado en: {output_models}")
    
    # 3b. Exportar DDLs individuales
    print("\n3b. Exportando DDLs individuales...")
    ddl_base_dir = r"C:\Users\jprodriguezm\ontology2db\DDLs"
    try:
        export_path = generator.export_ddl_to_files(schema, ddl_base_dir)
        print(f"   ✓ DDLs exportados en: {export_path}")
    except Exception as e:
        print(f"   ⚠ Error al exportar DDLs: {e}")

    # 4. Crear la base de datos
    print("\n4. Creando base de datos SQLite...")
    
    # Importar los modelos generados
    if os.path.basename(os.getcwd()) == 'examples':
        # Estamos en examples/
        sys.path.insert(0, '.')
        import generated_models
    else:
        # Estamos en raíz
        sys.path.insert(0, 'examples')
        import generated_models
    
    engine = generated_models.create_database(db_path)
    # Extraer nombre del archivo de la URL para mostrar
    db_file = db_path.replace("sqlite:///", "")
    print(f"   ✓ Base de datos creada: {db_file}")
    
    # 5. Exportar DDL
    print("\n5. DDL SQL generado:")
    print("   " + "="*60)
    generated_models.export_ddl(db_path)
    
    # 6. Generar visualizaciones
    print("\n6. Generando visualizaciones...")
    visualizer = OntologyVisualizer(ontology)
    
    # pyvis (HTML interactivo)
    try:
        html_output = "ontology_graph.html"
        visualizer.save_pyvis(html_output)
        print(f"   ✓ Visualización interactiva: {html_output}")
        print(f"     • Pasa el mouse sobre nodos para ver atributos")
        print(f"     • Pasa el mouse sobre relaciones para ver detalles")
    except ImportError as e:
        print(f"   ⚠ pyvis no disponible: {e}")
        print(f"     Instala con: pip install pyvis")
    except Exception as e:
        print(f"   ⚠ Error al generar HTML: {e}")
    
    # matplotlib (PNG estático)
    try:
        png_output = "ontology_graph.png"
        visualizer.save_matplotlib(png_output)
        print(f"   ✓ Visualización estática: {png_output}")
    except ImportError as e:
        print(f"   ⚠ matplotlib no disponible: {e}")
        print(f"     Instala con: pip install matplotlib")
    except Exception as e:
        print(f"   ⚠ Error al generar PNG: {e}")
    
    # Estadísticas del grafo
    print("\n7. Estadísticas del grafo:")
    visualizer.print_statistics()
    
    print("\n=== Proceso completado ===")
    print("\nPróximos pasos:")
    print(f"  1. Revisa el código generado en '{output_models}'")
    
    if os.path.basename(os.getcwd()) == 'examples':
        print(f"  2. Abre 'ontology_graph.html' en tu navegador")
    else:
        print(f"  2. Abre 'examples/ontology_graph.html' en tu navegador")
    
    print("  3. Usa los modelos en tu aplicación:")
    print("     from generated_models import Author, Book, get_session")
    
    print("\n✨ NOTA IMPORTANTE:")
    print("   Para ver los cambios en el navegador:")
    print("   • Abre en modo incógnito, O")
    print("   • Presiona Ctrl+Shift+R para recargar sin cache")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)