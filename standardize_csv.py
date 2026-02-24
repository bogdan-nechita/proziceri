#!/usr/bin/env python3
"""
CSV Standardization Script for Proziceri Proverbs

This script:
1. Adds a proper header row
2. Standardizes separator formatting (removes space padding)
3. Validates the output
4. Creates a clean, standard CSV file
"""

import sys
import csv
from pathlib import Path
from typing import List, Tuple

class ProverbCSVCleaner:
    """Clean and standardize the proverb CSV file"""

    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.data = []
        self.errors = []
        self.warnings = []

    def parse_original(self) -> List[Tuple[str, str, str]]:
        """Parse the original format and extract parts"""
        results = []

        with open(self.input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n')

                if not line:
                    continue

                part_one, separator, part_two = self._extract_parts(line, line_num)

                if part_one is not None and separator is not None and part_two is not None:
                    results.append((part_one, separator, part_two))
                else:
                    self.errors.append(f"Line {line_num}: Parsing error")

        return results

    def _extract_parts(self, line: str, line_num: int) -> Tuple[str, str, str]:
        """
        Extract the three parts from a proverb line.
        Handles multiple patterns including quoted content with embedded commas.
        """
        # Pattern 0: Quoted content with word separator like "content",word,"content"
        # This handles lines like: "Când eu cumpăr, nimeni nu vinde",când,"eu vând, nimeni nu cumpără."
        if line.startswith('"'):
            # Find the closing quote of the first part
            first_close = line.find('"', 1)
            if first_close > 0 and first_close + 1 < len(line) and line[first_close + 1] == ',':
                # Found "..." format, now find the separator word
                rest = line[first_close + 2:]  # Skip ","

                # Look for the pattern: word,"rest
                quote_pos = rest.find('"')
                if quote_pos > 0:
                    separator = rest[:quote_pos].rstrip(',')  # Remove trailing comma
                    # Find the closing quote of part_two
                    part_two_end = rest.rfind('"')
                    if part_two_end > quote_pos:
                        part_one = line[1:first_close]  # Remove quotes from part_one
                        part_two = rest[quote_pos + 1:part_two_end]  # Remove quotes from part_two
                        return part_one, separator, part_two

        # Pattern 1: Quoted separator like ,"",
        if ',",",' in line:
            parts = line.split(',",",' , 1)
            if len(parts) == 2:
                return parts[0], '","', parts[1]

        # Pattern 2: Space-padded separator like " , "
        if ' , ' in line:
            parts = line.split(' , ', 1)
            if len(parts) == 2:
                part_one = parts[0]
                part_two = parts[1]
                # Separator is a space in this case
                return part_one, ' ', part_two

        # Pattern 3: Regular comma separator (find first occurrence between words)
        comma_count = line.count(',')

        if comma_count >= 2:
            first_comma = line.find(',')
            second_comma = line.find(',', first_comma + 1)

            if first_comma != -1 and second_comma != -1:
                between = line[first_comma+1:second_comma]

                # Check if content between commas looks like a separator
                if len(between) <= 15:  # Reasonable separator length
                    part_one = line[:first_comma]
                    separator = between
                    part_two = line[second_comma+1:]
                    return part_one, separator, part_two

        # Pattern 4: Other punctuation separators (: or ;)
        for punct in [':,', ';,']:
            if punct in line:
                parts = line.split(punct, 1)
                if len(parts) == 2:
                    return parts[0], punct[0], parts[1]

        # Couldn't parse
        self.errors.append(f"Line {line_num}: Could not parse - {line[:60]}...")
        return None, None, None

    def normalize_separators(self, data: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """
        Normalize separators by:
        - Stripping whitespace from separators
        - Keeping the semantic content
        """
        normalized = []

        for part_one, separator, part_two in data:
            # Normalize the separator
            sep_normalized = separator.strip() if separator else ''

            # Special case: if separator is just spaces, keep one space
            if not sep_normalized and separator:
                sep_normalized = ' '

            # Strip leading/trailing spaces from parts
            part_one = part_one.strip() if part_one else ''
            part_two = part_two.strip() if part_two else ''

            normalized.append((part_one, sep_normalized, part_two))

        return normalized

    def write_csv(self, data: List[Tuple[str, str, str]]):
        """Write standardized CSV with header row"""
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(['part_one', 'separator', 'part_two'])

            # Write data
            for part_one, separator, part_two in data:
                writer.writerow([part_one, separator, part_two])

    def validate_output(self, data: List[Tuple[str, str, str]]) -> dict:
        """Validate the output"""
        stats = {
            'total_entries': len(data),
            'empty_separators': 0,
            'empty_parts': 0,
            'entries_with_commas': 0,
        }

        for part_one, separator, part_two in data:
            if not separator:
                stats['empty_separators'] += 1
            if not part_one or not part_two:
                stats['empty_parts'] += 1
            if ',' in part_one or ',' in part_two:
                stats['entries_with_commas'] += 1

        return stats

    def process(self):
        """Main processing pipeline"""
        print("=" * 70)
        print("PROZICERI CSV STANDARDIZATION")
        print("=" * 70)

        print(f"\n1. Parsing original file: {self.input_file}")
        data = self.parse_original()
        print(f"   ✓ Parsed {len(data)} entries")

        if self.errors:
            print(f"   ⚠ {len(self.errors)} parsing errors (will be skipped)")
            for error in self.errors[:3]:
                print(f"     - {error}")
            if len(self.errors) > 3:
                print(f"     ... and {len(self.errors) - 3} more")

        print(f"\n2. Normalizing separators...")
        normalized_data = self.normalize_separators(data)
        print(f"   ✓ Separators normalized")

        print(f"\n3. Validating output...")
        stats = self.validate_output(normalized_data)
        print(f"   ✓ Total entries: {stats['total_entries']}")
        if stats['empty_separators']:
            print(f"   ⚠ Entries with empty separators: {stats['empty_separators']}")
        if stats['empty_parts']:
            print(f"   ⚠ Entries with empty parts: {stats['empty_parts']}")

        print(f"\n4. Writing standardized CSV: {self.output_file}")
        self.write_csv(normalized_data)
        print(f"   ✓ File written successfully")

        print(f"\n5. Summary:")
        print(f"   - Header row: Added")
        print(f"   - Entries: {stats['total_entries']}")
        print(f"   - Separator normalization: Complete")
        print(f"   - Format: RFC 4180 CSV standard")
        print(f"   - Encoding: UTF-8")

        print("\n" + "=" * 70)
        print("Standardization complete! ✓")
        print("=" * 70)

        return normalized_data

def main():
    if len(sys.argv) < 3:
        print("Usage: python standardize_csv.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not Path(input_file).exists():
        print(f"Error: Input file not found - {input_file}")
        sys.exit(1)

    cleaner = ProverbCSVCleaner(input_file, output_file)
    cleaner.process()

if __name__ == '__main__':
    main()
