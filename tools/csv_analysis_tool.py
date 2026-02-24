#!/usr/bin/env python3
"""
CSV Analysis Tool for Proziceri Proverbs
Demonstrates parsing of original and improved CSV formats
"""

import csv
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class ProverbCSVAnalyzer:
    """Analyze and validate proverb CSV files"""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.data = []
        self.errors = []
        self.warnings = []

    def parse_original_format(self) -> List[Tuple[str, str, str]]:
        """
        Parse the original format where separator is embedded in the line.
        Format: part_one<separator>part_two

        Separators can be: comma, colon, semicolon, or quoted comma
        """
        results = []

        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n')

                # Skip empty lines
                if not line:
                    continue

                # Try to identify and split by separator
                part_one, separator, part_two = self._extract_parts(line, line_num)

                if part_one and part_two:
                    results.append((part_one, separator, part_two))

        return results

    def _extract_parts(self, line: str, line_num: int) -> Tuple[str, str, str]:
        """
        Extract the three parts from a proverb line.

        Handles multiple separator patterns:
        - Quoted separator: ","
        - Space-padded: " , "
        - Regular: ,
        - Other punctuation: : or ;
        """
        # Pattern 1: Quoted separator like ,"",
        if ',",",' in line:
            parts = line.split(',",",' , 1)
            if len(parts) == 2:
                return parts[0], '","', parts[1]

        # Pattern 2: Space-padded separator like " , "
        if ' , ' in line:
            parts = line.split(' , ', 1)
            if len(parts) == 2:
                return parts[0], ' , ', parts[1]

        # Pattern 3: Regular comma separator
        # Need to find the FIRST comma that's actually a separator
        # (not part of quoted content)
        comma_count = line.count(',')

        if comma_count >= 2:
            # Find first and second comma
            first_comma = line.find(',')
            second_comma = line.find(',', first_comma + 1)

            if first_comma != -1 and second_comma != -1:
                # Check if content between commas looks like a separator
                between = line[first_comma+1:second_comma]

                if len(between) <= 10:  # Likely a separator
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

        # Fallback: couldn't parse
        self.errors.append(f"Line {line_num}: Could not parse - {line[:50]}...")
        return "", "", ""

    def analyze_separators(self, data: List[Tuple[str, str, str]]) -> Dict:
        """Analyze separator patterns in the data"""
        separator_counts = {}

        for _, separator, _ in data:
            separator = separator.strip() if separator else ""
            separator_counts[separator] = separator_counts.get(separator, 0) + 1

        return separator_counts

    def validate_consistency(self, data: List[Tuple[str, str, str]]) -> Dict:
        """Check consistency issues"""
        issues = {
            'missing_parts': 0,
            'leading_trailing_space': 0,
            'empty_separator': 0,
        }

        for part_one, separator, part_two in data:
            if not part_one or not part_two:
                issues['missing_parts'] += 1

            if part_one != part_one.strip() or part_two != part_two.strip():
                issues['leading_trailing_space'] += 1

            if not separator or not separator.strip():
                issues['empty_separator'] += 1

        return issues

    def print_report(self):
        """Generate analysis report"""
        print("=" * 70)
        print("PROZICERI CSV ANALYSIS REPORT")
        print("=" * 70)

        # Parse file
        data = self.parse_original_format()

        print(f"\nFile: {self.filepath}")
        print(f"Total proverbs: {len(data)}")

        if self.errors:
            print(f"\nParsing Errors ({len(self.errors)}):")
            for error in self.errors[:5]:
                print(f"  - {error}")
            if len(self.errors) > 5:
                print(f"  ... and {len(self.errors) - 5} more")

        # Analyze separators
        print("\n" + "-" * 70)
        print("SEPARATOR ANALYSIS")
        print("-" * 70)
        separators = self.analyze_separators(data)

        for sep, count in sorted(separators.items(), key=lambda x: -x[1]):
            sep_display = repr(sep) if sep.strip() != sep else f"'{sep}'"
            print(f"  {sep_display:20} : {count:5} occurrences")

        # Consistency check
        print("\n" + "-" * 70)
        print("CONSISTENCY ANALYSIS")
        print("-" * 70)
        issues = self.validate_consistency(data)

        for issue, count in issues.items():
            if count > 0:
                print(f"  {issue:30} : {count}")

        # Sample entries
        print("\n" + "-" * 70)
        print("SAMPLE ENTRIES (First 5)")
        print("-" * 70)

        for i, (p1, sep, p2) in enumerate(data[:5], 1):
            print(f"\n  Entry {i}:")
            print(f"    Part 1: {p1}")
            print(f"    Sep:    {repr(sep)}")
            print(f"    Part 2: {p2}")

        # Recommendations
        print("\n" + "=" * 70)
        print("RECOMMENDATIONS FOR IMPROVEMENT")
        print("=" * 70)
        print("""
  1. ✓ Add CSV header row: part_one,separator,part_two
  2. ✓ Standardize all separators (remove padding spaces)
  3. ✓ Decide on quoting strategy for special separators
  4. ✓ Validate all 890 entries parse correctly
  5. ✓ Consider adding metadata columns: id, category, language
        """)
        print("=" * 70)

def main():
    if len(sys.argv) < 2:
        print("Usage: python csv_analysis_tool.py <csv_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"Error: File not found - {filepath}")
        sys.exit(1)

    analyzer = ProverbCSVAnalyzer(filepath)
    analyzer.print_report()

if __name__ == '__main__':
    main()
