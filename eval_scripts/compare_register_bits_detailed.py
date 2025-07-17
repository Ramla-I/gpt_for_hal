#!/usr/bin/env python3
"""
Enhanced script to compare two CSV files with register bit information and generate
detailed tables showing false positives and false negatives for RO, WO, and RW bits.

Usage: python compare_register_bits_detailed.py file1.csv file2.csv output.csv
"""

import csv
import sys
import re
from typing import Set, Dict, List, Tuple

def parse_bit_ranges(bit_string: str) -> Set[int]:
    """
    Parse a bit string like "1 3-7 10 13-15" into a set of individual bit numbers.
    Handles 'NA' values by returning an empty set.
    """
    if bit_string == 'NA' or not bit_string.strip():
        return set()
    
    bits = set()
    # Split by spaces and handle each part
    for part in bit_string.split():
        if '-' in part:
            # Handle ranges like "3-7"
            start, end = map(int, part.split('-'))
            bits.update(range(start, end + 1))
        else:
            # Handle single bits like "1"
            bits.add(int(part))
    
    return bits

def compare_bits(file1_bits: str, file2_bits: str) -> Tuple[Set[int], Set[int]]:
    """
    Compare bits between two files and return (false_positives, false_negatives).
    False positives: bits in file1 but not in file2
    False negatives: bits in file2 but not in file1
    """
    bits1 = parse_bit_ranges(file1_bits)
    bits2 = parse_bit_ranges(file2_bits)
    
    false_positives = bits1 - bits2  # In file1 but not in file2
    false_negatives = bits2 - bits1  # In file2 but not in file1
    
    return false_positives, false_negatives

def format_bit_set(bits: Set[int]) -> str:
    """Format a set of bits into a readable string representation."""
    if not bits:
        return "NA"
    
    # Convert to sorted list and format
    sorted_bits = sorted(bits)
    ranges = []
    start = end = sorted_bits[0]
    
    for bit in sorted_bits[1:]:
        if bit == end + 1:
            end = bit
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = end = bit
    
    # Handle the last range
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")
    
    return " ".join(ranges)

def compare_csv_files(file1_path: str, file2_path: str, output_path: str):
    """
    Compare two CSV files and generate a detailed comparison table.
    """
    # Read both CSV files
    data1 = {}
    data2 = {}
    
    # Read file1
    with open(file1_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            abbreviation = row['Abbreviation']
            data1[abbreviation] = {
                'RO': row['RO subfields'],
                'WO': row['WO subfields'],
                'RW': row['RW subfields']
            }
    
    # Read file2
    with open(file2_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            abbreviation = row['Abbreviation']
            data2[abbreviation] = {
                'RO': row['RO subfields'],
                'WO': row['WO subfields'],
                'RW': row['RW subfields']
            }
    
    # Find all unique abbreviations
    all_abbreviations = set(data1.keys()) | set(data2.keys())
    
    # Prepare output data
    output_rows = []
    summary_stats = {
        'RO': {'false_pos': 0, 'false_neg': 0},
        'WO': {'false_pos': 0, 'false_neg': 0},
        'RW': {'false_pos': 0, 'false_neg': 0}
    }
    
    for abbrev in sorted(all_abbreviations):
        row = {'Register': abbrev}
        
        # Get data for both files (use empty dict if not present)
        file1_data = data1.get(abbrev, {'RO': 'NA', 'WO': 'NA', 'RW': 'NA'})
        file2_data = data2.get(abbrev, {'RO': 'NA', 'WO': 'NA', 'RW': 'NA'})
        
        # Compare each bit type
        for bit_type in ['RO', 'WO', 'RW']:
            false_pos, false_neg = compare_bits(
                file1_data[bit_type], 
                file2_data[bit_type]
            )
            
            row[f'False_Positive_{bit_type}'] = format_bit_set(false_pos)
            row[f'False_Negative_{bit_type}'] = format_bit_set(false_neg)
            
            # Update summary statistics
            summary_stats[bit_type]['false_pos'] += len(false_pos)
            summary_stats[bit_type]['false_neg'] += len(false_neg)
        
        output_rows.append(row)
    
    # Write output CSV
    fieldnames = [
        'Register',
        'False_Positive_RO', 'False_Positive_WO', 'False_Positive_RW',
        'False_Negative_RO', 'False_Negative_WO', 'False_Negative_RW'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)
    
    print(f"Comparison completed. Results written to {output_path}")
    
    # Print detailed summary
    print("\n" + "="*80)
    print("DETAILED COMPARISON SUMMARY")
    print("="*80)
    
    total_false_pos = sum(stats['false_pos'] for stats in summary_stats.values())
    total_false_neg = sum(stats['false_neg'] for stats in summary_stats.values())
    
    print(f"\nOverall Statistics:")
    print(f"Total false positives: {total_false_pos}")
    print(f"Total false negatives: {total_false_neg}")
    
    print(f"\nBreakdown by Bit Type:")
    for bit_type in ['RO', 'WO', 'RW']:
        stats = summary_stats[bit_type]
        print(f"  {bit_type} bits:")
        print(f"    False positives: {stats['false_pos']}")
        print(f"    False negatives: {stats['false_neg']}")
    
    # Show registers with differences
    print(f"\nRegisters with Differences:")
    print("-" * 50)
    
    for row in output_rows:
        has_differences = False
        for bit_type in ['RO', 'WO', 'RW']:
            if (row[f'False_Positive_{bit_type}'] != 'NA' or 
                row[f'False_Negative_{bit_type}'] != 'NA'):
                has_differences = True
                break
        
        if has_differences:
            print(f"\n{row['Register']}:")
            for bit_type in ['RO', 'WO', 'RW']:
                fp = row[f'False_Positive_{bit_type}']
                fn = row[f'False_Negative_{bit_type}']
                if fp != 'NA' or fn != 'NA':
                    print(f"  {bit_type}: FP={fp}, FN={fn}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python compare_register_bits_detailed.py file1.csv file2.csv output.csv")
        print("Example: python compare_register_bits_detailed.py registers_table.csv registers_table_human_verified.csv comparison_results.csv")
        sys.exit(1)
    
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_path = sys.argv[3]
    
    try:
        compare_csv_files(file1_path, file2_path, output_path)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 