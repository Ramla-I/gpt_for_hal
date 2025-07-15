# Dependency Graph Generator

This Python script parses register operation code lines and generates a visual dependency graph.

## Format

The script expects code lines in the following format:
```
reg_info [depends reg_info]+
```

Where `reg_info` has the format:
```
[Operation(read or write) register_name <subfield_abbreviation subfield_range optional_value>+]
```

### Examples:
```
write PBS <rxa 4:0, txa 20:16> depends write PBA <rxa 4:0, txa 20:16>
write CTRL <SWRST 26 1> depends write PBS <rxa 4:0, txa 20:16>
write RCTL <EN 1 1> depends write RDH <NA 15:0> depends write CTRL <SWRST 26 1>
```

## Installation

1. Install required dependencies:
```bash
pip install -r requirements_graph.txt
```

## Usage

### Command Line

```bash
# Basic usage - displays the graph
python dependency_graph_generator.py input_file.txt

# Save graph to file
python dependency_graph_generator.py input_file.txt --output graph.png

# Save without displaying
python dependency_graph_generator.py input_file.txt --output graph.png --no-display
```

### Programmatic Usage

```python
from dependency_graph_generator import create_dependency_graph, visualize_graph

# Your code lines
code_lines = [
    "write PBS <rxa 4:0, txa 20:16> depends write PBA <rxa 4:0, txa 20:16>",
    "write CTRL <SWRST 26 1> depends write PBS <rxa 4:0, txa 20:16>"
]

# Create graph
G = create_dependency_graph(code_lines)

# Visualize
visualize_graph(G, "output.png")
```

## Features

- **Parsing**: Automatically parses register operations and their dependencies
- **Visualization**: Creates a directed graph with:
  - Blue nodes for read operations
  - Red nodes for write operations
  - Arrows showing dependency direction
- **Analysis**: Provides detailed analysis including:
  - Total nodes and edges
  - Operation counts
  - Cycle detection
  - Root and leaf node identification

## Output

The script generates:
1. **Console output**: Detailed analysis of the dependency graph
2. **Visual graph**: PNG image showing the dependency relationships
3. **Graph analysis**: Information about cycles, root nodes, and leaf nodes

## Example Output

```
=== DEPENDENCY GRAPH ANALYSIS ===
Total nodes: 7
Total edges: 6
Read operations: 0
Write operations: 7

No cycles found - dependencies are acyclic.

Root nodes (no dependencies): 1
  - write PBA <rxa 4:0, txa 20:16>

Leaf nodes (no dependents): 2
  - write RCTL <EN 1 1>
  - write TCTL <EN 1 1>
```

## Files

- `dependency_graph_generator.py`: Main script
- `requirements_graph.txt`: Python dependencies
- `example_usage.py`: Example programmatic usage
- `README_dependency_graph.md`: This documentation 