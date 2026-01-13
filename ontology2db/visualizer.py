"""Módulo visualizer"""

"""
Visualizador de ontologías como grafos.
"""
# ontology2db/visualizer.py
"""
Visualizador de ontologías como grafos.
"""
import html
import os
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
        """Construye el grafo preparando el HTML para el panel lateral."""
        
        # --- 1. PROCESAR CLASES (NODOS) ---
        for cls in self.ontology.classes:
            # Preparamos el HTML que irá DENTRO del panel lateral
            
            # Encabezado y Descripción
            safe_desc = html.escape(cls.description) if cls.description else "<i>Sin descripción</i>"
            
            # Inicio del contenido del panel
            panel_html = f"""
            <h2 style='margin-top:0; color:#2B7CE9; border-bottom: 1px solid #eee; padding-bottom: 10px;'>{cls.name}</h2>
            <div style='margin-bottom: 15px;'>
                <strong>Description:</strong><br>
                <span style='color: #555;'>{safe_desc}</span>
            </div>
            """
            
            # Tabla de Atributos
            if cls.attributes:
                panel_html += "<strong>Attributes:</strong><br>"
                panel_html += """
                <table style='width:100%; border-collapse: collapse; font-size: 13px; margin-top: 5px;'>
                    <tr style='background-color: #f2f2f2; text-align: left;'>
                        <th style='padding: 6px; border: 1px solid #ddd;'>Name</th>
                        <th style='padding: 6px; border: 1px solid #ddd;'>Type</th>
                        <th style='padding: 6px; border: 1px solid #ddd;'>Card.</th>
                        <th style='padding: 6px; border: 1px solid #ddd;'>Description</th>
                    </tr>
                """
                for attr in cls.attributes:
                    card = attr.cardinality if attr.cardinality != "1..1" else "1"
                    safe_desc = html.escape(attr.description) if attr.description else "<i>Sin descripción</i>"
                    panel_html += f"""
                    <tr>
                        <td style='padding: 6px; border: 1px solid #ddd;'><b>{attr.name}</b></td>
                        <td style='padding: 6px; border: 1px solid #ddd; color: #666;'>{attr.type}</td>
                        <td style='padding: 6px; border: 1px solid #ddd; text-align: center;'>{card}</td>
                        <td style='padding: 6px; border: 1px solid #ddd; color: #333;'>{safe_desc}</td>
                    </tr>
                    """
                panel_html += "</table>"
            else:
                panel_html += "<div style='padding:10px; color:#999; font-style:italic;'>No attributes</div>"

            panel_html += "<strong>Connected Relations:</strong>"
            
            # Filtramos relaciones donde esta clase sea origen o destino
            related = [r for r in self.ontology.relations if r.source == cls.name or r.target == cls.name]
            
            if related:
                panel_html += "<table style='border-color: #e0e0e0;'><thead><tr style='background:#f9f9f9;'><th>Source</th><th>Relation</th><th>Target</th></tr></thead><tbody>"
                for rel in related:
                    s_card = self._format_cardinality(rel.source_cardinality)
                    t_card = self._format_cardinality(rel.target_cardinality)
                    
                    # Resaltamos el nombre de la otra clase para que sea fácil de leer
                    source_display = f"<b>{rel.source}</b>" if rel.source == cls.name else rel.source
                    target_display = f"<b>{rel.target}</b>" if rel.target == cls.name else rel.target
                    
                    panel_html += f"""
                    <tr>
                        <td style='font-size:11px;'>{source_display} <small>({s_card})</small></td>
                        <td style='text-align:center; color:#2B7CE9; font-size:11px;'>-- {rel.name} --></td>
                        <td style='font-size:11px;'>{target_display} <small>({t_card})</small></td>
                    </tr>
                    """
                panel_html += "</tbody></table>"
            else:
                panel_html += "<p style='color:#999; font-style:italic;'>No connections</p>" 

            # Agregamos el nodo.
            # Nota: 'popup_html' es un atributo personalizado que usaremos con JS después.
            # Dejamos 'title' vacío o simple para que no moleste el tooltip nativo.
            self.graph.add_node(
                cls.name,
                label=cls.name,
                title="Click para ver detalles",  # Tooltip mínimo
                popup_html=panel_html,            # NUESTRO CONTENIDO HTML
                node_type="class",
                color="#97C2FC",
                font={'size': 14, 'face': 'arial', 'bold': True}
            )
        
        # --- 2. PROCESAR RELACIONES (ARISTAS) ---
        for rel in self.ontology.relations:
            source_card = self._format_cardinality(rel.source_cardinality)
            target_card = self._format_cardinality(rel.target_cardinality)
            label = f"[{source_card}]  {rel.name}  [{target_card}]"
            
            # HTML para el panel si se hace clic en la relación
            rel_html = f"""
            <h3 style='color:#666;'>Relación: {rel.name}</h3>
            <p><b>Tipo:</b> {rel.type}</p>
            <p>{rel.source} ⟶ {rel.target}</p>
            """
            if rel.description:
                rel_html += f"<p><i>{rel.description}</i></p>"

            edge_color = self._get_edge_color(rel.type)
            
            self.graph.add_edge(
                rel.source,
                rel.target,
                label=label,
                title="Click detalles",
                popup_html=rel_html, # Contenido para el panel
                color=edge_color,
                width=2,
                arrows={'to': {'enabled': True}}
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
        """Genera el grafo e inyecta el código para el panel lateral."""
        try:
            from pyvis.network import Network
        except ImportError:
            raise ImportError("Instala pyvis: pip install pyvis")
        
        # IMPORTANTE: notebook=False es necesario para que genere el JS correctamente
        net = Network(height="800px", width="100%", directed=True, bgcolor="#ffffff", font_color="#333333", notebook=False)
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
              "gravitationalConstant": -20000,
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
            "multiselect": false,
            "zoomView": true
          }
        }
        """)
        
        
        
        net.save_graph(output_file)
        self._inject_custom_js(output_file)
        print(f"✓ Visualización guardada en: {output_file}")
        print(f"  • Abre el archivo en tu navegador")
        print(f"  • Pasa el mouse sobre nodos para ver atributos")
        print(f"  • Pasa el mouse sobre relaciones para ver detalles")

    def _inject_custom_js(self, file_path: str):
        """Inyecta CSS y JS robusto para detectar la red y abrir el panel."""
        # 1. Calculamos los totales desde el objeto ontology antes de generar el HTML
        total_attrs = sum(len(cls.attributes) for cls in self.ontology.classes)
        total_nodes = len(self.ontology.classes)
        total_rels = len(self.ontology.relations)
        
        style_css = """
        <style>
            #side-panel {
                position: fixed; top: 0; left: -550px; width: 550px; height: 100%;
                background: white; box-shadow: 3px 0 15px rgba(0,0,0,0.3);
                padding: 25px; overflow-y: auto; transition: 0.4s; z-index: 9999;
                font-family: sans-serif; border-right: 5px solid #2B7CE9;
            }
            #side-panel.open { left: 0; }

            /* Estilo para la Tabla de Estadísticas Superior Derecha */
            #stats-counter {
                position: fixed; 
                top: 10px; 
                right: 10px;
                background: rgba(255, 255, 255, 0.9);
                padding: 10px; 
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
                z-index: 1000; 
                font-family: Arial, sans-serif;
                border: 1px solid #2B7CE9;
                width: auto;
            }
            #stats-counter table { border-collapse: collapse; margin-top: 0; }
            #stats-counter td { padding: 2px 8px; font-size: 12px; border: none; }
            .stat-val { font-weight: bold; color: #2B7CE9; text-align: right; }

            .close-btn { float: right; cursor: pointer; font-size: 28px; line-height: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 13px; }
            th { background-color: #f8f8f8; }
        </style>
        """

        stats_html = f"""
        <div id="stats-counter">
            <table>
                <tr><td>Nodos:</td><td class="stat-val">{total_nodes}</td></tr>
                <tr><td>Relaciones:</td><td class="stat-val">{total_rels}</td></tr>
                <tr><td>Atributos:</td><td class="stat-val">{total_attrs}</td></tr>
            </table>
        </div>
        """

        panel_html = """
        <div id="side-panel">
            <span style="float:right; cursor:pointer; font-size:24px;" onclick="document.getElementById('side-panel').classList.remove('open')">&times;</span>
            <div id="panel-content"></div>
        </div>
        """

        custom_js = """
        <script type="text/javascript">
            function initPanelIntegration() {
                // Pyvis suele llamar a la instancia 'network' o 'drawGraph'
                // Intentamos encontrar la instancia de la red de forma segura
                var networkInstance = window.network || window.drawGraph;
                
                if (!networkInstance) {
                    console.log("Esperando a que la red cargue...");
                    setTimeout(initPanelIntegration, 500);
                    return;
                }

                networkInstance.on("dragStart", function (params) {
                // Desactiva la física mientras arrastras para que el grafo no "baile"
                networkInstance.setOptions({ physics: { enabled: false } });
                });

                networkInstance.on("click", function (params) {
                    var panel = document.getElementById('side-panel');
                    var content = document.getElementById('panel-content');
                    
                    if (params.nodes.length > 0) {
                        var nodeId = params.nodes[0];
                        // Obtenemos los datos directamente del dataset de nodos
                        var data = nodes.get(nodeId);
                        if (data.popup_html) {
                            content.innerHTML = data.popup_html;
                            panel.classList.add('open');
                        }
                    } else {
                        panel.classList.remove('open');
                    }
                });
            }
            
            // Iniciar detección
            window.onload = initPanelIntegration;
        </script>
        """
        full_injection = style_css + stats_html + panel_html + custom_js
        
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Inyectar antes del cierre de la etiqueta body
        updated_html = html_content.replace('</body>', full_injection + '</body>')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
    
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