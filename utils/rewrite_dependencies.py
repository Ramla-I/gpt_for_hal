#!/usr/bin/env python3
"""
Rewrite dependency code lines in a more intuitive top-down style.
"""

from dependency_graph_generator import parse_code_line, create_dependency_graph
import networkx as nx

def analyze_dependency_flow(G: nx.DiGraph):
    """Analyze the dependency flow and return nodes in hierarchical order."""
    # Find root nodes (nodes with no incoming edges)
    root_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]
    
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
    
    # Group nodes by level
    nodes_by_level = {}
    for node, level in levels.items():
        if level not in nodes_by_level:
            nodes_by_level[level] = []
        nodes_by_level[level].append(node)
    
    # Sort nodes within each level for consistent ordering
    for level in nodes_by_level:
        nodes_by_level[level].sort()
    
    return nodes_by_level

def rewrite_code_lines(code_lines):
    """Rewrite code lines in top-down hierarchical order."""
    # Create dependency graph
    G = create_dependency_graph(code_lines)
    
    # Analyze dependency flow
    nodes_by_level = analyze_dependency_flow(G)
    
    # Create new code lines in top-down order
    new_code_lines = []
    
    # Process each level from top to bottom
    for level in sorted(nodes_by_level.keys()):
        level_nodes = nodes_by_level[level]
        
        for node in level_nodes:
            # Find all direct dependencies for this node
            dependencies = list(G.predecessors(node))
            
            if dependencies:
                # Create dependency chain for this node
                chain = [node] + dependencies
                # Reverse to show dependencies first, then the dependent node
                chain.reverse()
                
                # Format as code line
                code_line = " depends ".join(chain)
                new_code_lines.append(code_line)
            else:
                # Root node with no dependencies
                new_code_lines.append(f"# {node} (root node - no dependencies)")
    
    return new_code_lines

def main():
    # Read the original code lines
    input_file = "output/e1000/dependencies/extracted_code.txt"
    output_file = "output/e1000/dependencies/extracted_code_hierarchical.txt"
    
    try:
        with open(input_file, 'r') as f:
            original_lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return
    
    print("Original code lines:")
    for i, line in enumerate(original_lines, 1):
        print(f"{i}. {line}")
    
    print("\nRewriting in hierarchical order...")
    new_lines = rewrite_code_lines(original_lines)
    
    print("\nRewritten code lines (top-down):")
    for i, line in enumerate(new_lines, 1):
        print(f"{i}. {line}")
    
    # Write to new file
    with open(output_file, 'w') as f:
        for line in new_lines:
            f.write(line + '\n')
    
    print(f"\nRewritten code saved to: {output_file}")
    
    # Also create a more readable version with clear sections
    readable_file = "output/e1000/dependencies/extracted_code_readable.txt"
    with open(readable_file, 'w') as f:
        f.write("# Register Operation Dependencies (Top-Down Order)\n")
        f.write("# ===============================================\n\n")
        
        # Group by level
        G = create_dependency_graph(original_lines)
        nodes_by_level = analyze_dependency_flow(G)
        
        for level in sorted(nodes_by_level.keys()):
            level_nodes = nodes_by_level[level]
            f.write(f"# Level {level} - {'Root' if level == 0 else f'Dependent on Level {level-1}'}\n")
            f.write("# " + "-" * 50 + "\n")
            
            for node in level_nodes:
                dependencies = list(G.predecessors(node))
                if dependencies:
                    f.write(f"# {node}\n")
                    f.write(f"#   depends on: {', '.join(dependencies)}\n")
                    f.write(f"{node} depends {' depends '.join(dependencies)}\n\n")
                else:
                    f.write(f"# {node} (root - no dependencies)\n")
                    f.write(f"{node}\n\n")
    
    print(f"Readable version saved to: {readable_file}")

if __name__ == "__main__":
    main() 