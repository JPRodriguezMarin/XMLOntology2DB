"""Módulo cli"""

"""
Interfaz de línea de comandos.
"""
import argparse
import sys
from pathlib import Path
from .parser import OntologyParser
from .mapper import OntologyMapper
from .codegen import SQLAlchemyGenerator
from .visualizer import OntologyVisualizer


def main():
    """Función principal del CLI."""
    parser = argparse.ArgumentParser(
        description='Convierte ontologías XML a modelos SQLAlchemy'
    )
    
    parser.add_argument('input', help='Archivo XML de entrada')
    parser.add_argument('-o', '--output', default='models.py',
                       help='Archivo Python de salida (default: models.py)')
    parser.add_argument('-v', '--visualize', choices=['pyvis', 'matplotlib', 'both'],
                       help='Generar visualización')
    parser.add_argument('--viz-output', default='ontology_graph',
                       help='Nombre base para archivos de visualización')
    parser.add_argument('--no-models', action='store_true',
                       help='No generar modelos, solo visualización')
    
    args = parser.parse_args()
    
    # Verificar que el archivo existe
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: El archivo {args.input} no existe", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Parsear ontología
        print(f"Parseando {args.input}...")
        parser_obj = OntologyParser()
        ontology = parser_obj.parse(str(input_path))
        print(f"✓ Encontradas {len(ontology.classes)} clases y "
              f"{len(ontology.relations)} relaciones")
        
        # Generar modelos
        if not args.no_models:
            print(f"\nGenerando modelos SQLAlchemy...")
            mapper = OntologyMapper()
            schema = mapper.map(ontology)
            
            generator = SQLAlchemyGenerator()
            generator.generate(schema, args.output)
            print(f"✓ Modelos generados en: {args.output}")
        
        # Generar visualización
        if args.visualize:
            print(f"\nGenerando visualización...")
            visualizer = OntologyVisualizer(ontology)
            
            if args.visualize in ['pyvis', 'both']:
                output = f"{args.viz_output}.html"
                visualizer.save_pyvis(output)
            
            if args.visualize in ['matplotlib', 'both']:
                output = f"{args.viz_output}.png"
                visualizer.save_matplotlib(output)
        
        print("\n✓ Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()