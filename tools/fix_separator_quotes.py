#!/usr/bin/env python3
"""
Fix unnecessary quotes in CSV separators.

This script removes unnecessary quoting from separator values in the Proziceri CSV.
For example, converts """,""" to just , and """;""" to just ;
"""

import csv
import re
from pathlib import Path
from typing import Tuple, List


def unescape_separator(separator: str) -> str:
    """
    Remove unnecessary quotes from separator values.

    When a separator contains a comma or other special characters, csv.writer
    escapes it. This function removes those unnecessary escapes.

    Examples:
    - '","' (3 chars) -> ',' (comma was quoted)
    - ';"' (3 chars) -> ';' (semicolon was quoted)
    """
    if not separator:
        return separator

    # When csv.reader parses '","' from CSV, it becomes a 3-character string: quote-comma-quote
    # We need to extract just the middle character
    if len(separator) == 3 and separator[0] == '"' and separator[2] == '"':
        return separator[1]

    # If it's already a single character, return as is
    if len(separator) == 1:
        return separator

    return separator


def fix_csv(input_file: str, output_file: str):
    """Read CSV and fix separator quotes, write to output"""

    fixed_rows = []
    stats = {
        'total_rows': 0,
        'fixed_separators': 0,
    }

    # Read the input CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # Read header
        header = next(reader, None)
        if header:
            fixed_rows.append(header)

        # Read and process data rows
        for row in reader:
            stats['total_rows'] += 1

            if len(row) >= 3:
                part_one = row[0]
                separator = row[1]
                part_two = row[2]
                extra_fields = row[3:] if len(row) > 3 else []

                # Unescape the separator
                original_sep = separator
                separator = unescape_separator(separator)

                if separator != original_sep:
                    stats['fixed_separators'] += 1

                # Rebuild the row
                fixed_row = [part_one, separator, part_two] + extra_fields
                fixed_rows.append(fixed_row)
            else:
                fixed_rows.append(row)

    # Write the fixed CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(fixed_rows)

    return stats


def main():
    """Main entry point"""
    input_file = Path(__file__).parent.parent / "data" / "Proziceri.csv"
    output_file = Path(__file__).parent.parent / "data" / "Proziceri.csv"

    if not input_file.exists():
        print(f"Error: {input_file} not found")
        return 1

    print("=" * 70)
    print("FIXING CSV SEPARATOR QUOTES")
    print("=" * 70)
    print(f"\nProcessing: {input_file}")

    stats = fix_csv(str(input_file), str(output_file))

    print(f"\n✓ Processing complete!")
    print(f"  - Total rows processed: {stats['total_rows']}")
    print(f"  - Separators fixed: {stats['fixed_separators']}")
    print(f"\n✓ Output written to: {output_file}")
    print("\n" + "=" * 70)

    return 0


if __name__ == '__main__':
    exit(main())
