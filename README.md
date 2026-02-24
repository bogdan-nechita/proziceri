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
├── data/                    # Data Files
│   └── Proziceri.csv        # Cleaned, standardized proverbs (890 entries)
│
├── tests/                   # Tests
│   ├── proziceri.test.js    # JavaScript tests for core logic
│   └── test_csv_processing.py # Python tests for CSV processing
│
└── .gitignore
```

## Website Usage

The website loads proverbs from `data/Proziceri.csv` and generates dada sayings by:
1. Randomly selecting two proverbs
2. Splitting each at the separator
3. Combining the first half of one with the second half of the other

### Example
- Proverb 1: "Lupu-și schimbă părul dar năravul ba."
- Proverb 2: "Apa trece, pietrele rămân."
- **Generated**: "Lupu-și schimbă părul dar pietrele rămân."

## CSV Data Format

The `data/Proziceri.csv` contains standardized proverbs with:
- **part_one**: First part of the proverb
- **separator**: Connecting element (comma, space, etc.)
- **part_two**: Second part of the proverb

### Example Row
```csv
part_one,separator,part_two
Lupu-și schimbă părul dar,náravul ba,
Apa trece,,pietrele rămân.
```

## Running Tests

**Python tests:**
```bash
python3 -m unittest tests/test_csv_processing.py
```

**JavaScript tests:**
```bash
node tests/proziceri.test.js
```

## Running Locally

```bash
python3 -m http.server 8000
# Open http://localhost:8000/
```
