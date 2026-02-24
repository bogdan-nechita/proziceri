#!/usr/bin/env python3
"""
Enrich Proziceri CSV with metadata: ID and Category.

Adds:
- id: Unique identifier (1-890)
- category: Thematic classification based on keywords

Categories:
- wisdom: General wisdom and advice
- love: Love, relationships, marriage
- death: Death, mortality, fate
- nature: Animals, weather, seasons
- hardship: Suffering, pain, difficulty
- work: Labor, employment, trade
- divine: Divine providence, religion, fate
- social: Social commentary, people, society
- character: Behavior, virtues, vices
- wealth: Money, poverty, richness
"""

import csv
from pathlib import Path
from typing import Dict, List, Tuple


class ProverbEnricher:
    """Enrich proverbs with categories and IDs"""

    # Category keywords for heuristic classification
    KEYWORDS = {
        'wisdom': [
            'cuvânt', 'sfat', 'minte', 'rază', 'cuget', 'gândire', 'învață',
            'lecție', 'știință', 'cunoaștere', 'înțelepciune', 'deștept',
            'nebun', 'tare', 'slăb', 'bun', 'rău', 'drept', 'stricat'
        ],
        'love': [
            'iubire', 'iubește', 'dragoste', 'drag', 'soție', 'soț',
            'femeie', 'bărbat', 'inimă', 'suflet', 'tânără', 'tânăr',
            'frumos', 'frumoasă', 'frumusețe'
        ],
        'death': [
            'moarte', 'moare', 'mort', 'rămas', 'groaza', 'viu', 'viu',
            'vieață', 'nenorocit', 'condamnat'
        ],
        'nature': [
            'soare', 'lună', 'stea', 'plouă', 'ploaie', 'vânt', 'zăpadă',
            'apă', 'pădurea', 'copac', 'floare', 'pasăre', 'om', 'om',
            'cal', 'vacă', 'oaie', 'cioban', 'pescui', 'vânătoare',
            'animal', 'creștură', 'fiară'
        ],
        'hardship': [
            'necaz', 'nenorocire', 'suferință', 'dor', 'geană', 'trist',
            'tenebre', 'munk', 'chin', 'osânda', 'pedeapsa', 'blestem',
            'nedreptate', 'greșit', 'rău', 'greu', 'gursă'
        ],
        'work': [
            'muncă', 'muncitor', 'lucru', 'meșter', 'meserie', 'negustorie',
            'tîrgoveț', 'ciocan', 'mai', 'unealtă', 'plugar', 'grădinar',
            'vânzare', 'cumpărare', 'bani', 'monede', 'salară'
        ],
        'divine': [
            'Dumnezeu', 'Doamne', 'sfânt', 'sfântul', 'drac', 'iad', 'rai',
            'evanghel', 'biserică', 'preot', 'rugăciune', 'creștin',
            'păcatul', 'virtute', 'binecuvântat', 'blestem', 'Providence'
        ],
        'social': [
            'oameni', 'om', 'lume', 'popor', 'neam', 'verişti', 'vecin',
            'prieten', 'dușman', 'vrăjmașul', 'glas', 'gură', 'limba',
            'vorba', 'vorbire', 'tăcere'
        ],
        'character': [
            'mândrie', 'mândru', 'mândrețe', 'modest', 'modestie', 'curaj',
            'frică', 'invidios', 'invidie', 'răzbunare', 'datorită', 'cinstit',
            'necinstit', 'lacom', 'lăcomie', 'maliță', 'răutate', 'bunătate',
            'credință', 'necredincios', 'liniștit', 'neliniștit'
        ],
        'wealth': [
            'bani', 'bogat', 'bogăție', 'sărac', 'sărăcie', 'avere', 'moșie',
            'comerț', 'tranzacție', 'câștig', 'pierdere', 'profit', 'ruină',
            'credit', 'datornic', 'datorie'
        ]
    }

    def __init__(self, input_csv: str, output_csv: str):
        """Initialize enricher with input and output paths"""
        self.input_csv = Path(input_csv)
        self.output_csv = Path(output_csv)

    def categorize_proverb(self, part_one: str, separator: str, part_two: str) -> str:
        """
        Heuristically categorize a proverb based on keywords.

        Args:
            part_one: First part of proverb
            separator: Connecting element
            part_two: Second part of proverb

        Returns:
            Category name
        """
        full_text = f"{part_one} {separator} {part_two}".lower()

        # Count keyword matches for each category
        category_scores: Dict[str, int] = {cat: 0 for cat in self.KEYWORDS}

        for category, keywords in self.KEYWORDS.items():
            for keyword in keywords:
                if keyword in full_text:
                    category_scores[category] += 1

        # Return category with highest score, default to 'wisdom'
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        return 'wisdom'

    def enrich(self) -> Tuple[int, Dict[str, int]]:
        """
        Enrich CSV with ID and category columns.

        Returns:
            Tuple of (total_entries, category_counts)
        """
        enriched_data = []
        category_counts: Dict[str, int] = {cat: 0 for cat in self.KEYWORDS}

        # Read original CSV
        with open(self.input_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                part_one = row['part_one']
                separator = row['separator']
                part_two = row['part_two']

                # Determine category
                category = self.categorize_proverb(part_one, separator, part_two)
                category_counts[category] += 1

                # Add enriched row
                enriched_data.append({
                    'id': idx,
                    'part_one': part_one,
                    'separator': separator,
                    'part_two': part_two,
                    'category': category
                })

        # Write enriched CSV
        fieldnames = ['id', 'part_one', 'separator', 'part_two', 'category']
        with open(self.output_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(enriched_data)

        return len(enriched_data), category_counts

    def print_stats(self, total: int, category_counts: Dict[str, int]):
        """Print enrichment statistics"""
        print(f"\n{'='*70}")
        print(f"ENRICHMENT COMPLETE")
        print(f"{'='*70}")
        print(f"Total entries enriched: {total}")
        print(f"\nCategory Distribution:")
        print(f"{'-'*70}")

        # Sort by count descending
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100
            bar = '█' * int(percentage / 2)
            print(f"{category:15} {count:4} ({percentage:5.1f}%) {bar}")

        print(f"{'-'*70}")
        print(f"Output file: {self.output_csv}")
        print(f"Encoding: UTF-8 (RFC 4180 CSV)")
        print(f"{'='*70}\n")


def main():
    """Main entry point"""
    input_file = "../data/Proziceri.csv"
    output_file = "../data/Proziceri_enriched.csv"

    if not Path(input_file).exists():
        print(f"Error: {input_file} not found")
        return 1

    enricher = ProverbEnricher(input_file, output_file)

    print(f"Enriching {input_file}...")
    total, category_counts = enricher.enrich()
    enricher.print_stats(total, category_counts)

    return 0


if __name__ == '__main__':
    exit(main())
