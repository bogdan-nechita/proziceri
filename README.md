# Proziceri și Verbători

Proverbe și zicători românești cu un strop de dada (Romanian proverbs and sayings with a touch of dada)

## Project Structure

```
proziceri/
├── index.html                   # Entry point (redirects to website/)
├── website/                     # Website application
│   ├── index.html              # Main HTML page
│   ├── proziceri.js            # Core sayings generator
│   ├── proziceri.logic.js      # Text processing utilities
│   ├── proziceri.css           # Styling
│   ├── papaparse.min.js        # CSV parser
│   └── favicon.ico             # Website icon
├── data/
│   └── Proziceri.csv           # 890 Romanian proverbs (part_one, separator, part_two)
├── tests/
│   ├── proziceri.test.js       # JavaScript tests
│   ├── proziceri.logic.js      # Shared test utilities
│   └── test_csv_processing.py  # Python tests
├── jest.config.js              # Jest test configuration
├── DEPLOYMENT.md               # Deployment guide
└── .gitignore
```

## How It Works

The website generates dada sayings by:
1. Randomly selecting two proverbs from `data/Proziceri.csv`
2. Splitting each at the separator
3. Combining the first half of one with the second half of the other

**Example:**
- Proverb 1: "Lupu-și schimbă părul dar | năravul ba."
- Proverb 2: "Apa trece, | pietrele rămân."
- **Generated:** "Lupu-și schimbă părul dar | pietrele rămân."

## CSV Data Format

Each row contains:
- `part_one`: First part of the proverb
- `separator`: Connecting element (comma, space, etc.)
- `part_two`: Second part of the proverb

## Development

**Run JavaScript tests:**
```bash
npm test
# or
node tests/proziceri.test.js
```

**Run Python tests:**
```bash
python3 -m unittest tests/test_csv_processing.py
```

## Deployment

See `DEPLOYMENT.md` for deployment instructions.
