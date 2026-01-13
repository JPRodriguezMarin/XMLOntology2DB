"""Módulo visualizer"""

"""
Visualizador de ontologías como grafos.
"""
# ontology2db/visualizer.py
"""
Visualizador de ontologías como grafos - VERSIÓN CORREGIDA.
"""
import html
import networkx as nx
from typing import Optional
from .parser import Ontology


class OntologyVisualizer:
    """Visualiza ontologías como grafos."""
    
    def __init__(self, ontology: Ontology):
        """
        Inicializa el visualizador.
        
        Args:
            ontology: Ontología a visualizar
        """
        self.ontology = ontology
        self.graph = nx.DiGraph()
        self._build_graph()
    
    def _build_graph(self):
        """Construye el grafo desde la ontología."""
        # Agregar nodos para clases
        for cls in self.ontology.classes:
            # Crear tooltip con los atributos
            # 1. Class: Nombre
            safe_name = html.escape(cls.name)
            tooltip = f"<b>Class:</b> {safe_name}<br><br>"

            # 2. Description: Descripción (si existe)
            if cls.description:
                safe_desc = html.escape(cls.description)
                tooltip += f"<b>Description:</b> {safe_desc}<br><br>"
            
            # 3. Attributes: Lista
            if cls.attributes:
                tooltip += "<b>Attributes:</b><br>"
                attr_lines = []
                for attr in cls.attributes:
                    # Preparar datos del atributo
                    safe_attr_name = html.escape(attr.name)
                    safe_attr_type = html.escape(attr.type)
                    
                    # Formatear cardinalidad solo si no es "1"
                    card_str = f" [{attr.cardinality}]" if attr.cardinality != "1" else ""
                    
                    # Formato línea: • nombre: tipo [cardinalidad]
                    attr_lines.append(f"• {safe_attr_name}: {safe_attr_type}{card_str}")
                
                # Unir cada atributo con un salto de línea <br>
                tooltip += "<br>".join(attr_lines)
            else:
                tooltip += "<i>No attributes</i>"
            
            # Etiqueta simple para el nodo (solo nombre)
            self.graph.add_node(
                cls.name,
                label=cls.name,
                title=tooltip,  # Tooltip que aparece al hacer hover
                node_type="class",
                description=cls.description or "",
                size=30,
                color="#97C2FC",
                font={'size': 14, 'face': 'arial', 'bold': True}
            )
        
        # Agregar aristas para relaciones
        for rel in self.ontology.relations:
            # Formatear cardinalidades correctamente
            source_card = self._format_cardinality(rel.source_cardinality)
            target_card = self._format_cardinality(rel.target_cardinality)
            
            # Etiqueta: [cardinalidad_origen] nombre [cardinalidad_destino]
            # Sin saltos de línea, todo en una línea
            label = f"[{source_card}]  {rel.name}  [{target_card}]"
            
            # Tooltip con información adicional
            tooltip = f"<b>Relation:</b> {rel.name}<br>"
            tooltip += f"<b>Type:</b> {rel.type}<br><br>"
            tooltip += f"{rel.source} [{source_card}] → [{target_card}] {rel.target}"
            if rel.description:
                tooltip += f"<br><br><b>Description:</b> {rel.description}"
            
            if rel.properties:
                tooltip += "<br><br><b>Properties:</b><br>"
                prop_lines = []
                for prop in rel.properties:
                    prop_lines.append(f"• {prop.name}: {prop.type} [{prop.cardinality}]")
                tooltip += "<br>".join(prop_lines)
            
            # Color según tipo de relación
            edge_color = self._get_edge_color(rel.type)
            
            self.graph.add_edge(
                rel.source,
                rel.target,
                label=label,
                title=tooltip,  # Tooltip al hacer hover
                relation_type=rel.type,
                color=edge_color,
                width=2,
                arrows={'to': {'enabled': True, 'scaleFactor': 1.2}},
                font={'size': 11, 'align': 'horizontal'}
            )
    
    def _format_cardinality(self, cardinality: str) -> str:
        """
        Formatea la cardinalidad para mostrarla correctamente.
        
        Args:
            cardinality: Cardinalidad sin formatear (ej: "0..n", "1", "1..1")
            
        Returns:
            Cardinalidad formateada (ej: "0..*", "1", "1")
        """
        # Normalizar la cardinalidad
        cardinality = cardinality.strip()
        
        # Reemplazar 'n' por '*' para consistencia
        if cardinality.endswith('n'):
            cardinality = cardinality[:-1] + '*'
        
        # Casos especiales
        if cardinality == "1..1":
            return "1"
        elif cardinality == "*":
            return "*"
        elif cardinality == "0..*":
            return "*"
        elif cardinality == "1..*":
            return "1..*"
        
        return cardinality
    
    def _get_edge_color(self, relation_type: str) -> str:
        """
        Retorna el color de la arista según el tipo de relación.
        
        Args:
            relation_type: Tipo de relación
            
        Returns:
            Color en formato hex
        """
        colors = {
            'association': '#848484',      # Gris
            'aggregation': '#4A90E2',      # Azul
            'composition': '#E24A4A',      # Rojo
            'inheritance': '#50C878',      # Verde
        }
        return colors.get(relation_type.lower(), '#848484')
    
    def save_pyvis(self, output_file: str = "ontology_graph.html"):
        """
        Guarda el grafo como HTML interactivo usando pyvis.
        
        Args:
            output_file: Ruta del archivo HTML de salida
        """
        try:
            from pyvis.network import Network
        except ImportError:
            raise ImportError("pyvis no está instalado. Ejecuta: pip install pyvis")
        
        # Crear red con opciones mejoradas
        net = Network(
            height="800px", 
            width="100%", 
            directed=True,
            notebook=False,
            bgcolor="#ffffff",
            font_color="#333333"
        )
        
        # Transferir el grafo a pyvis
        net.from_nx(self.graph)
        
        # Configurar física y opciones
        net.set_options("""
        {
          "nodes": {
            "shape": "box",
            "borderWidth": 2,
            "borderWidthSelected": 3,
            "shadow": {
              "enabled": true,
              "size": 5
            },
            "font": {
              "size": 14,
              "face": "arial",
              "bold": {
                "color": "#000000"
              }
            },
            "margin": 10
          },
          "edges": {
            "arrows": {
              "to": {
                "enabled": true,
                "scaleFactor": 1.2
              }
            },
            "smooth": {
              "enabled": true,
              "type": "cubicBezier",
              "roundness": 0.5
            },
            "font": {
              "size": 11,
              "align": "horizontal",
              "background": "rgba(255, 255, 255, 0.8)",
              "strokeWidth": 0
            },
            "shadow": {
              "enabled": false
            }
          },
          "physics": {
            "enabled": true,
            "barnesHut": {
              "gravitationalConstant": -15000,
              "centralGravity": 0.3,
              "springLength": 200,
              "springConstant": 0.04,
              "damping": 0.09,
              "avoidOverlap": 0.5
            },
            "minVelocity": 0.75,
            "solver": "barnesHut",
            "stabilization": {
              "enabled": true,
              "iterations": 1000,
              "updateInterval": 25
            }
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 100,
            "navigationButtons": true,
            "keyboard": {
              "enabled": true
            },
            "multiselect": true,
            "zoomView": true
          }
        }
        """)
        
        # Agregar título y leyenda
        net.heading = "Visualización de Ontología"
        
        net.save_graph(output_file)
        print(f"✓ Visualización guardada en: {output_file}")
        print(f"  • Abre el archivo en tu navegador")
        print(f"  • Pasa el mouse sobre nodos para ver atributos")
        print(f"  • Pasa el mouse sobre relaciones para ver detalles")
    
    def save_matplotlib(self, output_file: str = "ontology_graph.png"):
        """
        Guarda el grafo como imagen usando matplotlib.
        
        Args:
            output_file: Ruta del archivo de imagen de salida
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("matplotlib no está instalado. "
                            "Ejecuta: pip install matplotlib")
        
        plt.figure(figsize=(16, 12))
        
        # Layout mejorado
        pos = nx.spring_layout(self.graph, k=3, iterations=50, seed=42)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(
            self.graph, 
            pos, 
            node_color='#97C2FC',
            node_size=4000, 
            alpha=0.9,
            edgecolors='#2B7CE9',
            linewidths=2
        )
        
        # Dibujar aristas con colores según tipo
        for edge in self.graph.edges(data=True):
            source, target, data = edge
            color = data.get('color', '#848484')
            relation_type = data.get('relation_type', 'association')
            
            # Estilo según tipo
            if relation_type == 'composition':
                style = 'solid'
                width = 3
            elif relation_type == 'aggregation':
                style = 'dashed'
                width = 2
            else:
                style = 'solid'
                width = 2
            
            nx.draw_networkx_edges(
                self.graph, 
                pos,
                edgelist=[(source, target)],
                edge_color=color,
                arrows=True,
                arrowsize=25,
                width=width,
                style=style,
                arrowstyle='->'
            )
        
        # Etiquetas de nodos (solo nombres)
        node_labels = {node: node for node in self.graph.nodes()}
        nx.draw_networkx_labels(
            self.graph, 
            pos, 
            node_labels, 
            font_size=11,
            font_weight='bold',
            font_family='sans-serif'
        )
        
        # Etiquetas de aristas (nombre + cardinalidades)
        edge_labels = {}
        for source, target, data in self.graph.edges(data=True):
            label = data.get('label', '')
            # Para matplotlib, limitar longitud si es muy largo
            if len(label) > 30:
                label = label[:27] + "..."
            edge_labels[(source, target)] = label
        
        nx.draw_networkx_edge_labels(
            self.graph, 
            pos, 
            edge_labels,
            font_size=9,
            font_family='sans-serif',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none')
        )
        
        # Leyenda
        legend_elements = [
            plt.Line2D([0], [0], color='#848484', linewidth=2, label='Asociación'),
            plt.Line2D([0], [0], color='#4A90E2', linewidth=2, linestyle='--', label='Agregación'),
            plt.Line2D([0], [0], color='#E24A4A', linewidth=3, label='Composición'),
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        plt.title("Diagrama de Ontología", fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Visualización guardada en: {output_file}")
        plt.close()
    
    def export_statistics(self) -> dict:
        """
        Exporta estadísticas del grafo.
        
        Returns:
            Diccionario con estadísticas
        """
        stats = {
            'num_classes': self.graph.number_of_nodes(),
            'num_relations': self.graph.number_of_edges(),
            'avg_degree': sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes() if self.graph.number_of_nodes() > 0 else 0,
            'density': nx.density(self.graph),
        }
        
        # Tipos de relaciones
        relation_types = {}
        for _, _, data in self.graph.edges(data=True):
            rel_type = data.get('relation_type', 'unknown')
            relation_types[rel_type] = relation_types.get(rel_type, 0) + 1
        
        stats['relation_types'] = relation_types
        
        return stats
    
    def print_statistics(self):
        """Imprime estadísticas del grafo."""
        stats = self.export_statistics()
        
        print("\n" + "="*60)
        print("  ESTADÍSTICAS DEL GRAFO")
        print("="*60)
        print(f"  Clases:              {stats['num_classes']}")
        print(f"  Relaciones:          {stats['num_relations']}")
        print(f"  Grado promedio:      {stats['avg_degree']:.2f}")
        print(f"  Densidad:            {stats['density']:.4f}")
        print("\n  Tipos de relaciones:")
        for rel_type, count in stats['relation_types'].items():
            print(f"    • {rel_type.capitalize()}: {count}")
        print("="*60 + "\n")