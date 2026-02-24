# Proziceri și Verbători

Proverbe și zicători românești cu un strop de dada (Romanian proverbs and sayings with a touch of dada)

## Project Structure

```
proziceri/
├── index.html               # Main HTML page
├── proziceri.js             # Core logic for generating dada sayings
├── proziceri.logic.js       # Utility functions for text processing
├── proziceri.css            # Styling
├── papaparse.min.js         # CSV parsing library
├── favicon.ico              # Website icon
│
├── data/                        # 📊 Data Files
│   └── Proziceri.csv            # Cleaned, standardized proverbs (890 entries)
│
├── tools/                       # 🔧 Internal Tools & Scripts
│   ├── csv_analysis_tool.py     # Analyze and report on CSV data
│   ├── standardize_csv.py       # Standardize CSV format (add headers, normalize)
│   ├── fix_empty_separators.py  # Fix entries with empty/problematic separators
│   └── enrich_csv.py            # Add ID and category metadata to proverbs
│
├── tests/                       # ✅ Tests
│   ├── proziceri.test.js        # JavaScript tests for core logic
│   └── test_csv_processing.py   # Python tests for CSV processing
│
├── docs/                        # 📚 Documentation
│   ├── ANALYSIS_SUMMARY.md      # Summary of data analysis
│   ├── CSV_IMPROVEMENTS.md      # Details on CSV improvements
│   ├── STANDARDIZATION_REPORT.md # CSV standardization details
│   ├── EMPTY_SEPARATOR_FIX_REPORT.md # Separator fix details
│   ├── ENRICHMENT_GUIDE.md      # Guide for enriching CSV with metadata
│   └── TEST_REPORT.md           # Test coverage and results
│
└── .gitignore                   # Git ignore rules
```

## Website Usage

The website loads proverbs from `data/Proziceri.csv` (served from the project root) and generates dada sayings by:
1. Randomly selecting two proverbs
2. Splitting each at the separator
3. Combining the first half of one with the second half of the other

### Example
- Proverb 1: "Lupu-și schimbă părul dar năravul ba."
- Proverb 2: "Apa trece, pietrele rămân."
- **Generated**: "Lupu-și schimbă părul dar pietrele rămân."

## CSV Data Format

The active `data/Proziceri.csv` contains standardized proverbs with:
- **part_one**: First part of the proverb
- **separator**: Connecting element (comma, space, etc.)
- **part_two**: Second part of the proverb

### Example Row
```csv
part_one,separator,part_two
Lupu-și schimbă părul dar,náravul ba,
Apa trece,,pietrele rămân.
```

## Tools & Development

### Running Tools

**Analyze CSV data:**
```bash
python3 tools/csv_analysis_tool.py
```

**Standardize CSV (if modifying data):**
```bash
python3 tools/standardize_csv.py input.csv output.csv
```

**Add metadata (ID + categories) to CSV:**
```bash
python3 tools/enrich_csv.py
```

**Fix separator issues:**
```bash
python3 tools/fix_empty_separators.py
```

### Running Tests

**Python tests:**
```bash
python3 -m unittest tests/test_csv_processing.py
```

**JavaScript tests:**
```bash
# Open tests/proziceri.test.js in browser or run with Node.js
node tests/proziceri.test.js
```

## Data Management

- **Active Data**: `data/Proziceri.csv` - This is what the website uses
- **Enriched Data**: Optional enhanced version with IDs and categories (generate with `tools/enrich_csv.py`)

### Data Statistics
- **Total Entries**: 890 proverbs
- **Format**: CSV with standardized headers
- **Encoding**: UTF-8
- **Status**: Cleaned and validated

## Deployment

To deploy:
1. Serve the project root via a web server
2. Open `index.html` to run the site locally
3. The website loads `data/Proziceri.csv` automatically
4. Deploy the project root to a web server

## Contributing

When modifying the CSV data:
1. Always work with tools in the `tools/` directory
2. Update `data/Proziceri.csv` only through standardization
3. Run tests to validate changes
4. Update documentation as needed
