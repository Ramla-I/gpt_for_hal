#!/usr/bin/env python3
"""
Dependency Graph Generator for Register Operations

This script parses code lines in the format:
reg_info [depends reg_info]+

where reg_info has the format:
[Operation(read or write) register_name <subfield_abbreviation subfield_range optional_value>+]

And creates a visual dependency graph.
"""

import re
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any
import argparse
import os

class RegisterInfo:
    """Represents a register operation with its details."""
    
    def __init__(self, operation: str, register_name: str, subfields: List[Dict[str, str]]):
        self.operation = operation
        self.register_name = register_name
        self.subfields = subfields
    
    def __str__(self) -> str:
        subfield_str = ", ".join([f"{sf['abbreviation']} {sf['range']}" + 
                                 (f" {sf['value']}" if sf.get('value') else "") 
                                 for sf in self.subfields])
        return f"{self.operation} {self.register_name} <{subfield_str}>"
    
    def get_label(self) -> str:
        """Get a shorter label for the graph node."""
        subfield_str = ", ".join([sf['abbreviation'] for sf in self.subfields])
        return f"{self.operation}\n{self.register_name}\n{subfield_str}"

def parse_subfields(subfield_text: str) -> List[Dict[str, str]]:
    """Parse subfield information from text like 'rxa 4:0, txa 20:16' or 'SWRST 26 1'."""
    subfields = []
    
    # Split by comma and handle each subfield
    parts = [part.strip() for part in subfield_text.split(',')]
    
    for part in parts:
        # Split by space to get abbreviation, range, and optional value
        tokens = part.split()
        if len(tokens) >= 2:
            abbreviation = tokens[0]
            range_val = tokens[1]
            value = tokens[2] if len(tokens) > 2 else None
            
            subfields.append({
                'abbreviation': abbreviation,
                'range': range_val,
                'value': value
            })
    
    return subfields

def parse_register_info(reg_info_text: str) -> RegisterInfo:
    """Parse a register info string into a RegisterInfo object."""
    # Match pattern: operation register_name <subfields>
    pattern = r'(read|write)\s+(\w+)\s+<(.+?)>'
    match = re.match(pattern, reg_info_text.strip())
    
    if not match:
        raise ValueError(f"Invalid register info format: {reg_info_text}")
    
    operation = match.group(1)
    register_name = match.group(2)
    subfields_text = match.group(3)
    
    subfields = parse_subfields(subfields_text)
    
    return RegisterInfo(operation, register_name, subfields)

def parse_code_line(line: str) -> List[RegisterInfo]:
    """Parse a code line and return a list of RegisterInfo objects in dependency order."""
    # Split by 'depends' to get the dependency chain
    parts = [part.strip() for part in line.split('depends')]
    
    register_infos = []
    for part in parts:
        if part:  # Skip empty parts
            reg_info = parse_register_info(part)
            register_infos.append(reg_info)
    
    return register_infos

def create_dependency_graph(code_lines: List[str]) -> nx.DiGraph:
    """Create a directed graph from the code lines."""
    G = nx.DiGraph()
    
    for line in code_lines:
        if line.strip():
            register_infos = parse_code_line(line)
            
            # Add nodes for each register info
            for reg_info in register_infos:
                node_id = str(reg_info)
                G.add_node(node_id, label=reg_info.get_label(), 
                          operation=reg_info.operation,
                          register=reg_info.register_name)
            
            # Add edges for dependencies (from dependent to dependee)
            for i in range(len(register_infos) - 1):
                dependent = str(register_infos[i])
                dependee = str(register_infos[i + 1])
                G.add_edge(dependee, dependent)
    
    return G

def visualize_graph(G: nx.DiGraph, output_file: str = None):
    """Visualize the dependency graph."""
    plt.figure(figsize=(14, 10))
    
    # Create a hierarchical layout with root nodes at the top
    pos = create_hierarchical_layout(G)
    
    # Draw nodes with different colors for read/write operations
    read_nodes = [node for node, data in G.nodes(data=True) if data.get('operation') == 'read']
    write_nodes = [node for node, data in G.nodes(data=True) if data.get('operation') == 'write']
    
    nx.draw_networkx_nodes(G, pos, nodelist=read_nodes, node_color='lightblue', 
                          node_size=3000, alpha=0.7)
    nx.draw_networkx_nodes(G, pos, nodelist=write_nodes, node_color='lightcoral', 
                          node_size=3000, alpha=0.7)
    
    # Draw edges with straight lines and arrows pointing to node edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20,
                          connectionstyle="arc3,rad=0.05", arrowstyle='->',
                          node_size=3000, width=2)  # Thicker edges for better visibility
    
    # Draw labels
    labels = {node: data['label'] for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    plt.title("Register Operation Dependency Graph", fontsize=16, fontweight='bold')
    plt.axis('off')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightblue', label='Read Operations'),
        Patch(facecolor='lightcoral', label='Write Operations')
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Graph saved to {output_file}")
    else:
        plt.show()

def create_hierarchical_layout(G: nx.DiGraph):
    """Create a hierarchical layout with root nodes at the top."""
    # Find root nodes (nodes with no incoming edges)
    root_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]
    
    # If no root nodes, use regular layout
    if not root_nodes:
        try:
            return nx.kamada_kawai_layout(G)
        except:
            return nx.spring_layout(G, k=4, iterations=100)
    
    # Calculate levels for each node
    levels = {}
    visited = set()
    
    # Start with root nodes at level 0
    current_level = 0
    current_nodes = set(root_nodes)
    
    while current_nodes:
        # Assign current level to all nodes in current_nodes
        for node in current_nodes:
            levels[node] = current_level
            visited.add(node)
        
        # Find next level nodes (children of current nodes)
        next_nodes = set()
        for node in current_nodes:
            for neighbor in G.successors(node):
                if neighbor not in visited:
                    # Check if all predecessors of this neighbor are visited
                    if all(pred in visited for pred in G.predecessors(neighbor)):
                        next_nodes.add(neighbor)
        
        current_nodes = next_nodes
        current_level += 1
    
    # Assign remaining nodes to the highest level
    for node in G.nodes():
        if node not in levels:
            levels[node] = current_level
    
    # Create positions based on levels
    pos = {}
    max_level = max(levels.values()) if levels else 0
    
    for level in range(max_level + 1):
        level_nodes = [n for n, l in levels.items() if l == level]
        level_nodes.sort()  # Sort for consistent ordering
        
        # Position nodes horizontally within their level
        for i, node in enumerate(level_nodes):
            x = (i - len(level_nodes) / 2) * 2  # Spread nodes horizontally
            y = max_level - level  # Root nodes at top (y=0), leaf nodes at bottom
            pos[node] = (x, y)
    
    return pos

def print_dependency_analysis(G: nx.DiGraph):
    """Print analysis of the dependency graph."""
    print("\n=== DEPENDENCY GRAPH ANALYSIS ===")
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    
    # Count operations
    read_count = len([n for n, d in G.nodes(data=True) if d.get('operation') == 'read'])
    write_count = len([n for n, d in G.nodes(data=True) if d.get('operation') == 'write'])
    print(f"Read operations: {read_count}")
    print(f"Write operations: {write_count}")
    
    # Find cycles
    try:
        cycles = list(nx.simple_cycles(G))
        if cycles:
            print(f"\nWARNING: Found {len(cycles)} cycle(s) in dependencies!")
            for i, cycle in enumerate(cycles):
                print(f"Cycle {i+1}: {' -> '.join(cycle)}")
        else:
            print("\nNo cycles found - dependencies are acyclic.")
    except nx.NetworkXNoCycle:
        print("\nNo cycles found - dependencies are acyclic.")
    
    # Find root nodes (nodes with no incoming edges)
    root_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]
    print(f"\nRoot nodes (no dependencies): {len(root_nodes)}")
    for node in root_nodes:
        print(f"  - {node}")
    
    # Find leaf nodes (nodes with no outgoing edges)
    leaf_nodes = [n for n in G.nodes() if G.out_degree(n) == 0]
    print(f"\nLeaf nodes (no dependents): {len(leaf_nodes)}")
    for node in leaf_nodes:
        print(f"  - {node}")

def main():
    parser = argparse.ArgumentParser(description='Generate dependency graph from register operation code lines')
    parser.add_argument('input_file', help='Input file containing code lines')
    parser.add_argument('--output', '-o', help='Output file for the graph image (optional)')
    parser.add_argument('--no-display', action='store_true', help='Do not display the graph (only save if output specified)')
    
    args = parser.parse_args()
    
    # Read input file
    try:
        with open(args.input_file, 'r') as f:
            code_lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        return
    
    # Remove empty lines and strip whitespace
    code_lines = [line.strip() for line in code_lines if line.strip()]
    
    print(f"Parsing {len(code_lines)} code lines...")
    
    try:
        # Create dependency graph
        G = create_dependency_graph(code_lines)
        
        # Print analysis
        print_dependency_analysis(G)
        
        # Visualize graph
        if args.output or not args.no_display:
            visualize_graph(G, args.output)
        
    except Exception as e:
        print(f"Error processing code lines: {e}")
        return

if __name__ == "__main__":
    main() 