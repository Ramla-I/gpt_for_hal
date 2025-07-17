#!/usr/bin/env python3
"""
Example usage of the dependency graph generator.
"""

from dependency_graph_generator import parse_code_line, create_dependency_graph, visualize_graph, print_dependency_analysis

def main():
    # Example code lines
    code_lines = [
        "write PBS <rxa 4:0, txa 20:16> depends write PBA <rxa 4:0, txa 20:16>",
        "write CTRL <SWRST 26 1> depends write PBS <rxa 4:0, txa 20:16>",
        "write RCTL <EN 1 1> depends write RDH <NA 15:0> depends write CTRL <SWRST 26 1>",
        "write TCTL <EN 1 1> depends write TDH <NA 15:0> depends write CTRL <SWRST 26 1>"
    ]
    
    print("Example code lines:")
    for i, line in enumerate(code_lines, 1):
        print(f"{i}. {line}")
    
    print("\nParsing individual lines:")
    for i, line in enumerate(code_lines, 1):
        print(f"\nLine {i}:")
        register_infos = parse_code_line(line)
        for j, reg_info in enumerate(register_infos):
            print(f"  {j+1}. {reg_info}")
            print(f"     Operation: {reg_info.operation}")
            print(f"     Register: {reg_info.register_name}")
            print(f"     Subfields: {reg_info.subfields}")
    
    print("\nCreating dependency graph...")
    G = create_dependency_graph(code_lines)
    
    # Print analysis
    print_dependency_analysis(G)
    
    # Visualize the graph
    print("\nGenerating graph visualization...")
    visualize_graph(G, "example_dependency_graph.png")
    
    print("\nGraph saved as 'example_dependency_graph.png'")

if __name__ == "__main__":
    main() 