import ast
import xml.etree.ElementTree as ET
import os

def python_to_ontology_xml():
    ruta_entrada = r"C:\Users\jprodriguezm\ontology2db\CyberDEM\__init__.py"
    directorio_destino = r"C:\Users\jprodriguezm\ontology2db\CyberDEM"
    ruta_salida = os.path.join(directorio_destino, "CyberDEM_Ontology.xml")

    with open(ruta_entrada, "r", encoding="utf-8") as file:
        node = ast.parse(file.read())

    root = ET.Element("Ontology")
    
    # Listas para procesar después
    clases_info = []
    relaciones_encontradas = []

    # 1. Primer pase: Extraer clases y herencia
    for item in node.body:
        if isinstance(item, ast.ClassDef):
            clases_info.append(item)
            # Si hereda de algo que no sea 'object', creamos una relación de herencia
            for base in item.bases:
                if isinstance(base, ast.Name) and base.id not in ['object', 'dict']:
                    relaciones_encontradas.append({
                        "source": item.name,
                        "target": base.id,
                        "type": "is_a"
                    })

    # 2. Generar XML de Clases
    for item in clases_info:
        class_el = ET.SubElement(root, "Class", name=item.name)
        
        # Descripción
        doc = ast.get_docstring(item)
        desc_el = ET.SubElement(class_el, "description")
        desc_el.text = doc.strip() if doc else f"CyberDEM {item.name}"

        # Atributos
        attrs_node = ET.SubElement(class_el, "Attributes")
        
        # PK única para evitar el error de SQLAlchemy anterior
        pk_name = f"{item.name.lower()}_id"
        pk_el = ET.SubElement(attrs_node, "Attribute", name=pk_name, type="integer", cardinality="1")
        pk_el.set("primary_key", "true")

        # Buscar atributos que terminen en '_id' (suelen ser claves foráneas/relaciones)
        found_vars = set(['id', 'kwargs', 'args', 'self'])
        for subnode in item.body:
            if isinstance(subnode, ast.FunctionDef) and subnode.name == "__init__":
                for arg in subnode.args.args:
                    name = arg.arg
                    if name not in found_vars:
                        ET.SubElement(attrs_node, "Attribute", name=name, type="string", cardinality="1")
                        
                        # Si el atributo parece una relación (ej. related_event_id)
                        if name.endswith('_id') and name != pk_name:
                            relaciones_encontradas.append({
                                "source": item.name,
                                "target": name.replace('_id', '').capitalize(), # Intento de adivinar destino
                                "type": "references"
                            })
                        found_vars.add(name)

    # 3. SECCIÓN DE RELACIONES (Crucial para el Visualizer y el Mapper)
    relations_node = ET.SubElement(root, "Relations")
    for rel in relaciones_encontradas:
        # Solo añadimos la relación si el destino existe en nuestro archivo
        rel_el = ET.SubElement(relations_node, "Relation", 
                               name=rel["type"], 
                               source=rel["source"], 
                               target=rel["target"])

    # Guardar
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)
    print(f"✅ XML con {len(relaciones_encontradas)} relaciones generado.")

if __name__ == "__main__":
    python_to_ontology_xml()