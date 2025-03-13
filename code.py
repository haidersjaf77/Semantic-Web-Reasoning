from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, FOAF, DCTERMS, XSD
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

# Define namespaces
EX = Namespace('http://example.org/university/')
UNI = Namespace('http://example.org/university/ontology/')

# Create an RDF graph
g = Graph()

# Bind prefixes to namespaces
g.bind('ex', EX)
g.bind('foaf', FOAF)
g.bind('dcterms', DCTERMS)
g.bind('uni', UNI)

# URIRefs
imran_khan = EX['ImranKhan']
student1 = EX['Student1']
student2 = EX['Student2']
student3 = EX['Student3']
course1 = EX['Course1']
course2 = EX['Course2']
course3 = EX['Course3']
professor = EX['Professor']

# Literals
imran_khan_name = Literal('Imran Khan', datatype=XSD.string)
student1_name = Literal('xxx', datatype=XSD.string)
student2_name = Literal('yyy', datatype=XSD.string)
student3_name = Literal('zzz', datatype=XSD.string)
course1_title = Literal('Knowledge Reasoning and Representation', datatype=XSD.string)
course2_title = Literal('Machine Learning', datatype=XSD.string)
course3_title = Literal('Knowledgebase Management System', datatype=XSD.string)
professor_name = Literal('ppp', datatype=XSD.string)

# Add triples to the graph
g.add((imran_khan, RDF.type, UNI.Leader))
g.add((imran_khan, FOAF.name, imran_khan_name))

g.add((student1, RDF.type, UNI.Student))
g.add((student1, FOAF.name, student1_name))
g.add((student1, UNI.follows, imran_khan))

g.add((student2, RDF.type, UNI.Student))
g.add((student2, FOAF.name, student2_name))
g.add((student2, UNI.follows, imran_khan))

g.add((student3, RDF.type, UNI.Student))
g.add((student3, FOAF.name, student3_name))
g.add((student3, UNI.follows, imran_khan))

g.add((course1, RDF.type, UNI.Course))
g.add((course1, DCTERMS.title, course1_title))

g.add((course2, RDF.type, UNI.Course))
g.add((course2, DCTERMS.title, course2_title))

g.add((course3, RDF.type, UNI.Course))
g.add((course3, DCTERMS.title, course3_title))

g.add((professor, RDF.type, UNI.Professor))
g.add((professor, FOAF.name, professor_name))
g.add((professor, UNI.follows, imran_khan))

g.add((student1, UNI.enrolledIn, course1))
g.add((student2, UNI.enrolledIn, course2))
g.add((student3, UNI.enrolledIn, course3))
g.add((professor, UNI.teaches, course1))
g.add((professor, UNI.teaches, course2))
g.add((professor, UNI.teaches, course3))

# Convert RDF graph to NetworkX graph
def rdf_to_networkx(graph):
    G = nx.DiGraph()

    for s, p, o in graph:
        s_label = s.split('/')[-1]
        p_label = p.split('/')[-1]
        if p_label == 'type':
            continue  # Skip rdf-syntax-ns#type
        o_label = o.split('/')[-1] if isinstance(o, URIRef) else str(o)

        G.add_node(s_label)
        if isinstance(o, URIRef):
            G.add_node(o_label)
            G.add_edge(s_label, o_label, label=p_label)
        else:
            G.add_node(o_label, shape='box', style='filled', fillcolor='yellow')
            G.add_edge(s_label, o_label, label=p_label)

    return G

# Load the image of Imran Khan
imran_khan_img = Image.open('imran_khan.jpg')

# Function to draw the image on the plot
def add_image(image, ax, position, zoom=0.1):
    imagebox = OffsetImage(image, zoom=zoom)
    ab = AnnotationBbox(imagebox, position, frameon=False)
    ax.add_artist(ab)

# Visualize the graph
def visualize_graph(G):
    pos = nx.spring_layout(G, seed=42, k=1.7)  # Increase the k value for more spacing
    edge_labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(15, 10))  # Increase the figure size
    ax = plt.gca()

    # Draw nodes with different colors and shapes based on type
    node_color_map = {
        'ImranKhan': 'gold',
        'Student1': 'lightblue',
        'Student2': 'lightblue',
        'Student3': 'lightblue',
        'Professor': 'lightcoral',
        'Course1': 'lightgreen',
        'Course2': 'lightgreen',
        'Course3': 'lightgreen'
    }

    node_shape_map = {
        'ImranKhan': 'o',
        'Student1': 'o',
        'Student2': 'o',
        'Student3': 'o',
        'Professor': 'o',
        'Course1': 's',
        'Course2': 's',
        'Course3': 's'
    }

    node_sizes = {
        'ImranKhan': 3000,
        'Student1': 2000,
        'Student2': 2000,
        'Student3': 2000,
        'Professor': 2000,
        'Course1': 2000,
        'Course2': 2000,
        'Course3': 2000
    }

    for node in G.nodes:
        nx.draw_networkx_nodes(
            G, pos, nodelist=[node], node_size=node_sizes.get(node, 1000),
            node_color=node_color_map.get(node, 'lightgrey'), node_shape=node_shape_map.get(node, 'o'),
            edgecolors='black', ax=ax
        )

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.6, edge_color='black')

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)

    # Clean edge labels
    edge_labels_cleaned = {key: value for key, value in edge_labels.items() if value != 'type'}
    # Draw edge labels with increased transparency
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_cleaned, font_color='red', font_size=12, alpha=0.5, ax=ax)

    # Add the image of Imran Khan at his node's position
    add_image(imran_khan_img, ax, pos['ImranKhan'], zoom=0.1)

    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Leader', markerfacecolor='gold', markersize=15),
        plt.Line2D([0], [0], marker='o', color='w', label='Student', markerfacecolor='lightblue', markersize=15),
        plt.Line2D([0], [0], marker='o', color='w', label='Professor', markerfacecolor='lightcoral', markersize=15),
        plt.Line2D([0], [0], marker='s', color='w', label='Course', markerfacecolor='lightgreen', markersize=15)
    ]
    ax.legend(handles=legend_elements, loc='best', fontsize=12)

    plt.title('University RDF Graph Visualization', fontsize=16)
    plt.axis('off')  # Hide axes
    plt.show()

# Create NetworkX graph from RDF
nx_graph = rdf_to_networkx(g)

# Visualize NetworkX graph
visualize_graph(nx_graph)
