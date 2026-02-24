#!/usr/bin/env python3
"""
Fix entries with empty or problematic separators in the standardized CSV.

This script:
1. Identifies entries with empty separators
2. Fixes entries with double commas (separator should be comma)
3. Validates space separators are intentional
4. Maintains data integrity
"""

import csv
from pathlib import Path
from typing import List, Tuple

def fix_empty_separators(input_file: str, output_file: str):
    """Fix entries with empty or problematic separators"""

    # Read the CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print("=" * 70)
    print("FIXING EMPTY SEPARATORS")
    print("=" * 70)

    fixes_made = 0
    issues = {
        'double_comma_fixed': [],
        'space_separators': [],
        'empty_kept': []
    }

    # Process each row
    for idx, row in enumerate(rows, 1):
        sep = row['separator']
        part_one = row['part_one']
        part_two = row['part_two']

        # Case 1: Completely empty separator
        if sep == '' or (sep and sep.isspace()):
            # Check if this came from a double comma in original
            # These are entries 477 and 827
            if idx == 477:  # "Numai când moare omul" - double comma originally
                row['separator'] = ','
                issues['double_comma_fixed'].append((idx, part_one, part_two))
                fixes_made += 1
                print(f"\n✓ Entry {idx}: Fixed double-comma separator")
                print(f"  Part 1: {part_one}")
                print(f"  Sep:    ',' (comma)")
                print(f"  Part 2: {part_two}")
            elif idx == 827:  # "Omul fără boi" - double comma originally
                row['separator'] = ','
                issues['double_comma_fixed'].append((idx, part_one, part_two))
                fixes_made += 1
                print(f"\n✓ Entry {idx}: Fixed double-comma separator")
                print(f"  Part 1: {part_one}")
                print(f"  Sep:    ',' (comma)")
                print(f"  Part 2: {part_two}")
            else:
                # Space separators are intentional (from original " , " pattern)
                if sep == ' ':
                    issues['space_separators'].append((idx, part_one, part_two))
                else:
                    issues['empty_kept'].append((idx, part_one, part_two))

    # Write the fixed CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['part_one', 'separator', 'part_two'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\n✓ Double-comma separators fixed: {len(issues['double_comma_fixed'])}")
    print(f"  - These entries now use comma as the separator")

    print(f"\n✓ Space separators preserved: {len(issues['space_separators'])}")
    print(f"  - These are intentional (from original ' , ' pattern)")
    print(f"  - Examples: Entry 16, 17, 26, 33, etc.")

    if issues['empty_kept']:
        print(f"\n⚠ Other cases: {len(issues['empty_kept'])}")
        for idx, p1, p2 in issues['empty_kept'][:3]:
            print(f"  - Entry {idx}: '{p1}' __ '{p2}'")

    print(f"\nTotal fixes applied: {fixes_made}")
    print(f"Output file: {output_file}")
    print("=" * 70)

def main():
    input_file = '../data/Proziceri.csv'
    output_file = '../data/Proziceri_fixed.csv'

    if not Path(input_file).exists():
        print(f"Error: {input_file} not found")
        return

    fix_empty_separators(input_file, output_file)

if __name__ == '__main__':
    main()
