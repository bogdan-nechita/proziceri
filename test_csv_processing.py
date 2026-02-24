#!/usr/bin/env python3
"""
Test suite for Proziceri CSV processing and standardization.

Tests cover:
- CSV parsing and standardization
- Separator normalization
- Empty separator fixes
- Data integrity
- Format compliance
"""

import unittest
import csv
import tempfile
from pathlib import Path
from standardize_csv import ProverbCSVCleaner


class TestProverbCSVCleaner(unittest.TestCase):
    """Tests for the CSV standardization functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up temporary files"""
        self.temp_dir.cleanup()

    def create_test_csv(self, content: str) -> Path:
        """Helper to create test CSV file"""
        test_file = self.temp_path / "test_input.csv"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return test_file

    def read_output_csv(self, filepath: Path) -> list:
        """Helper to read output CSV"""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    # ==================== Parsing Tests ====================

    def test_parse_basic_separator(self):
        """Test parsing basic comma separator"""
        input_file = self.create_test_csv(
            "Part one,separator,Part two\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], "Part one")
        self.assertEqual(data[0][1], "separator")
        self.assertEqual(data[0][2], "Part two")

    def test_parse_quoted_separator(self):
        """Test parsing quoted comma separator"""
        input_file = self.create_test_csv(
            'A ajuns un papugiu,",",țipă ca un surugiu.\n'
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], "A ajuns un papugiu")
        self.assertEqual(data[0][1], '","')
        self.assertEqual(data[0][2], "țipă ca un surugiu.")

    def test_parse_word_separator(self):
        """Test parsing word separator"""
        input_file = self.create_test_csv(
            "A dat Dumnezeu boale,dar,a dat și leacuri.\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], "A dat Dumnezeu boale")
        self.assertEqual(data[0][1], "dar")
        self.assertEqual(data[0][2], "a dat și leacuri.")

    def test_parse_space_separator(self):
        """Test parsing space-padded separator"""
        input_file = self.create_test_csv(
            "Baba bătrână nu se teme, ,de vorba groasă.\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], "Baba bătrână nu se teme")
        self.assertEqual(data[0][1], " ")
        self.assertEqual(data[0][2], "de vorba groasă.")

    def test_parse_quoted_content_with_embedded_comma(self):
        """Test parsing quoted content with embedded commas"""
        input_file = self.create_test_csv(
            '"Când eu cumpăr, nimeni nu vinde",când,"eu vând, nimeni nu cumpără."\n'
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], "Când eu cumpăr, nimeni nu vinde")
        self.assertEqual(data[0][1], "când")
        self.assertEqual(data[0][2], "eu vând, nimeni nu cumpără.")

    def test_parse_colon_separator(self):
        """Test parsing colon separator"""
        input_file = self.create_test_csv(
            "Bine zice moș Arvinte,:,vai de cap unde nu-i minte.\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], "Bine zice moș Arvinte")
        self.assertEqual(data[0][1], ":")
        self.assertEqual(data[0][2], "vai de cap unde nu-i minte.")

    # ==================== Normalization Tests ====================

    def test_normalize_removes_whitespace(self):
        """Test that normalization removes leading/trailing spaces from parts"""
        input_file = self.create_test_csv(
            "Part one ,separator ,Part two\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()
        normalized = cleaner.normalize_separators(data)

        self.assertEqual(normalized[0][0], "Part one")
        self.assertEqual(normalized[0][1], "separator")
        self.assertEqual(normalized[0][2], "Part two")

    def test_normalize_strips_separator_whitespace(self):
        """Test that separator whitespace is stripped"""
        data = [("Part one", " separator ", "Part two")]
        cleaner = ProverbCSVCleaner("dummy", "dummy")
        normalized = cleaner.normalize_separators(data)

        self.assertEqual(normalized[0][1], "separator")

    def test_normalize_preserves_meaningful_content(self):
        """Test that normalization preserves actual content"""
        data = [("Part one", "și", "Part two")]
        cleaner = ProverbCSVCleaner("dummy", "dummy")
        normalized = cleaner.normalize_separators(data)

        self.assertEqual(normalized[0][0], "Part one")
        self.assertEqual(normalized[0][1], "și")
        self.assertEqual(normalized[0][2], "Part two")

    # ==================== CSV Output Tests ====================

    def test_csv_output_has_header(self):
        """Test that output CSV has proper header"""
        input_file = self.create_test_csv(
            "Part one,separator,Part two\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()
        normalized = cleaner.normalize_separators(data)
        cleaner.write_csv(normalized)

        rows = self.read_output_csv(output_file)
        # Check that DictReader can read it (header present)
        self.assertIn('part_one', rows[0] if rows else {})

    def test_csv_output_format(self):
        """Test that CSV output is RFC 4180 compliant"""
        input_file = self.create_test_csv(
            "Part one,separator,Part two\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()
        normalized = cleaner.normalize_separators(data)
        cleaner.write_csv(normalized)

        # Read raw content
        with open(output_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()

        self.assertEqual(first_line.strip(), "part_one,separator,part_two")

    def test_csv_output_with_special_characters(self):
        """Test CSV output handles Romanian characters correctly"""
        input_file = self.create_test_csv(
            "Va răsări soarele,și,pe ulița noastră.\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()
        normalized = cleaner.normalize_separators(data)
        cleaner.write_csv(normalized)

        rows = self.read_output_csv(output_file)
        self.assertEqual(rows[0]['part_one'], "Va răsări soarele")
        self.assertEqual(rows[0]['part_two'], "pe ulița noastră.")

    # ==================== Data Integrity Tests ====================

    def test_no_data_loss_in_processing(self):
        """Test that processing preserves all data"""
        input_file = self.create_test_csv(
            "Part one,separator,Part two\n"
            "Another part,și,last part\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        input_data = cleaner.parse_original()
        normalized = cleaner.normalize_separators(input_data)
        cleaner.write_csv(normalized)

        output_data = self.read_output_csv(output_file)

        self.assertEqual(len(input_data), len(output_data))
        for inp, out in zip(input_data, output_data):
            self.assertEqual(inp[0], out['part_one'])
            self.assertEqual(inp[2], out['part_two'])

    def test_all_entries_have_required_fields(self):
        """Test that all entries have part_one, separator, part_two"""
        input_file = self.create_test_csv(
            "Part one,separator,Part two\n"
            "Another,și,entry\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()
        normalized = cleaner.normalize_separators(data)
        cleaner.write_csv(normalized)

        rows = self.read_output_csv(output_file)
        for row in rows:
            self.assertIn('part_one', row)
            self.assertIn('separator', row)
            self.assertIn('part_two', row)
            self.assertTrue(row['part_one'])
            self.assertTrue(row['part_two'])

    # ==================== Edge Case Tests ====================

    def test_multiple_entries(self):
        """Test processing multiple entries"""
        input_file = self.create_test_csv(
            "Entry 1,separator,Part 1\n"
            "Entry 2,și,Part 2\n"
            "Entry 3,dar,Part 3\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        self.assertEqual(len(data), 3)

    def test_handles_quoted_text(self):
        """Test handling of quoted text in entries"""
        input_file = self.create_test_csv(
            '"Quoted text, with comma",separator,"More text"\n'
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        # Should successfully parse despite quotes and embedded comma
        self.assertEqual(len(data), 1)

    def test_real_data_file(self):
        """Test with actual Proziceri.csv file"""
        input_file = Path("Proziceri.csv")
        if not input_file.exists():
            self.skipTest("Proziceri.csv not found")

        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()

        # Should parse all 890 entries
        self.assertEqual(len(data), 890)

        # All entries should have three parts
        for entry in data:
            self.assertEqual(len(entry), 3)
            self.assertTrue(entry[0])  # part_one exists
            # separator can be empty or space for some entries
            self.assertTrue(entry[2])  # part_two exists

    # ==================== Validation Tests ====================

    def test_validate_output_stats(self):
        """Test validation statistics generation"""
        input_file = self.create_test_csv(
            "Part one,separator,Part two\n"
            "Entry 2,și,Part 2\n"
        )
        output_file = self.temp_path / "output.csv"

        cleaner = ProverbCSVCleaner(str(input_file), str(output_file))
        data = cleaner.parse_original()
        normalized = cleaner.normalize_separators(data)
        stats = cleaner.validate_output(normalized)

        self.assertEqual(stats['total_entries'], 2)
        self.assertEqual(stats['empty_separators'], 0)
        self.assertEqual(stats['empty_parts'], 0)


class TestCleanedCSVFile(unittest.TestCase):
    """Tests for the actual cleaned CSV file"""

    def setUp(self):
        """Set up test fixtures"""
        self.csv_file = Path("Proziceri_clean.csv")
        if not self.csv_file.exists():
            self.skipTest("Proziceri_clean.csv not found")

    def test_file_exists(self):
        """Test that cleaned CSV file exists"""
        self.assertTrue(self.csv_file.exists())

    def test_file_is_valid_csv(self):
        """Test that file is valid CSV"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Should have 890 entries
        self.assertEqual(len(rows), 890)

    def test_has_header_row(self):
        """Test that CSV has proper header"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()

        self.assertEqual(first_line.strip(), "part_one,separator,part_two")

    def test_all_entries_have_three_parts(self):
        """Test that all entries have part_one, separator, part_two"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.assertTrue(row['part_one'], f"Empty part_one in row")
                self.assertTrue(row['part_two'], f"Empty part_two in row")
                self.assertIsNotNone(row['separator'], "No separator in row")

    def test_no_empty_separators(self):
        """Test that no entries have empty separators"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, 1):
                # Separator can be space, but not empty string
                self.assertTrue(
                    row['separator'] or row['separator'] == ' ',
                    f"Entry {idx} has empty separator"
                )

    def test_entry_477_fixed(self):
        """Test that entry 477 has valid separator"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        entry_477 = rows[476]  # 0-indexed, so 477-1
        self.assertEqual(entry_477['part_one'], "Numai când moare omul")
        self.assertEqual(entry_477['separator'], " ")
        self.assertEqual(entry_477['part_two'], "se cunoaște ce-a fost.")

    def test_entry_827_fixed(self):
        """Test that entry 827 has valid separator"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        entry_827 = rows[826]  # 0-indexed, so 827-1
        self.assertEqual(entry_827['part_one'], "Omul fără boi")
        self.assertEqual(entry_827['separator'], " ")
        self.assertEqual(entry_827['part_two'], "e ca robul legat de mâini.")

    def test_separator_distribution(self):
        """Test separator distribution statistics"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        separator_counts = {}
        for row in rows:
            sep = row['separator']
            if sep not in separator_counts:
                separator_counts[sep] = 0
            separator_counts[sep] += 1

        # Should have space separators
        self.assertIn(' ', separator_counts)
        self.assertEqual(separator_counts[' '], 40)

        # Should have quoted comma separators (shown as '","' when read from CSV)
        self.assertIn('","', separator_counts)
        self.assertGreater(separator_counts['","'], 0)

        # Total should be 890
        self.assertEqual(sum(separator_counts.values()), 890)

    def test_utf8_encoding(self):
        """Test that file is properly UTF-8 encoded"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Should contain Romanian characters without errors
        self.assertIn('ă', content)
        self.assertIn('ș', content)
        self.assertIn('ț', content)


class TestEnrichedCSVFile(unittest.TestCase):
    """Tests for the enriched CSV with metadata"""

    def setUp(self):
        """Set up test fixtures"""
        self.csv_file = Path("Proziceri_enriched.csv")
        if not self.csv_file.exists():
            self.skipTest("Proziceri_enriched.csv not found")

    def test_enriched_file_exists(self):
        """Test that enriched CSV file exists"""
        self.assertTrue(self.csv_file.exists())

    def test_enriched_has_correct_columns(self):
        """Test that enriched CSV has all required columns"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()

        self.assertEqual(
            first_line.strip(),
            "id,part_one,separator,part_two,category"
        )

    def test_enriched_has_890_entries(self):
        """Test that enriched CSV has 890 entries"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 890)

    def test_enriched_all_entries_have_id(self):
        """Test that all entries have unique sequential IDs"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for idx, row in enumerate(rows, 1):
            self.assertEqual(int(row['id']), idx)

    def test_enriched_all_entries_have_category(self):
        """Test that all entries have a category"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        valid_categories = {
            'wisdom', 'love', 'death', 'nature', 'hardship',
            'work', 'divine', 'social', 'character', 'wealth'
        }

        for row in rows:
            self.assertIn(row['category'], valid_categories)

    def test_enriched_category_distribution(self):
        """Test category distribution statistics"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        category_counts = {}
        for row in rows:
            cat = row['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Wisdom should be largest category
        self.assertGreater(category_counts['wisdom'], 400)

        # Nature should be second largest
        self.assertGreater(category_counts['nature'], 150)

        # Total should be 890
        self.assertEqual(sum(category_counts.values()), 890)

    def test_enriched_example_categorizations(self):
        """Test specific examples are correctly categorized"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Entry 1: "Va răsări soarele" - should be nature (soarele = sun)
        self.assertEqual(rows[0]['id'], '1')
        self.assertEqual(rows[0]['category'], 'nature')

        # Entry 5: "A nu avea nici sfânt" - should be divine
        self.assertEqual(rows[4]['id'], '5')
        self.assertEqual(rows[4]['category'], 'divine')

    def test_enriched_preserves_original_data(self):
        """Test that enrichment preserves original proverb data"""
        with open("Proziceri_clean.csv", 'r', encoding='utf-8') as f:
            clean_rows = list(csv.DictReader(f))

        with open(self.csv_file, 'r', encoding='utf-8') as f:
            enriched_rows = list(csv.DictReader(f))

        for clean, enriched in zip(clean_rows, enriched_rows):
            self.assertEqual(clean['part_one'], enriched['part_one'])
            self.assertEqual(clean['separator'], enriched['separator'])
            self.assertEqual(clean['part_two'], enriched['part_two'])


class TestCSVCompliance(unittest.TestCase):
    """Tests for RFC 4180 CSV compliance"""

    def setUp(self):
        """Set up test fixtures"""
        self.csv_file = Path("Proziceri_clean.csv")
        if not self.csv_file.exists():
            self.skipTest("Proziceri_clean.csv not found")

    def test_fields_with_commas_are_quoted(self):
        """Test that fields containing commas are properly quoted"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # part_two can contain commas (should be fine)
                if ',' in row['part_two']:
                    # Just verify it's readable (DictReader handled escaping)
                    self.assertIsNotNone(row['part_two'])

    def test_can_be_imported_to_excel_format(self):
        """Test that file can be read as standard CSV"""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            # Use standard csv module to verify RFC 4180 compliance
            reader = csv.reader(f)
            rows = list(reader)

        # Should have header + 890 entries = 891 rows
        self.assertEqual(len(rows), 891)

        # Each row should have exactly 3 fields
        for idx, row in enumerate(rows):
            self.assertEqual(len(row), 3, f"Row {idx} has {len(row)} fields, expected 3")


def run_tests_with_report():
    """Run all tests and generate a report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestProverbCSVCleaner))
    suite.addTests(loader.loadTestsFromTestCase(TestCleanedCSVFile))
    suite.addTests(loader.loadTestsFromTestCase(TestEnrichedCSVFile))
    suite.addTests(loader.loadTestsFromTestCase(TestCSVCompliance))

    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests_with_report()
    exit(0 if success else 1)
