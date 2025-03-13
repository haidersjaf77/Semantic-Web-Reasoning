# Semantic-Web-Reasoning

# University RDF Graph Visualization  

## Overview  
This project explores **RDF (Resource Description Framework)** and **RDFS (RDF Schema)** for semantic data representation. Using **Python's rdflib**, an RDF graph is created to model relationships between individuals, courses, and a professor. The graph is then converted into a **NetworkX** structure and visualized using **Matplotlib**.

## Features  
- **RDF Graph Creation**: Defines nodes (students, professor, courses) and relationships.  
- **Ontology Modeling**: Uses namespaces, literals, and RDF triples for structured data representation.  
- **Graph Conversion & Visualization**: Converts RDF data to **NetworkX** for advanced visualization with customized node colors and shapes.  
- **Interactive Display**: Supports Pyvis for interactive web-based graph exploration.  

## Technologies Used  
- **Python** (rdflib, NetworkX, Matplotlib)  
- **RDF & RDFS** for structured data modeling  
- **Pyvis** (optional) for interactive visualization  

## How to Run  
1. Install dependencies:  
   ```bash
   pip install rdflib networkx matplotlib pillow pyvis
