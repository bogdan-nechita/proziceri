# Proziceri CSV Enrichment Guide

## Overview

The enriched CSV format adds **metadata** to the standardized proverbs, making them suitable for databases, applications, and advanced analysis.

## New Format

**File**: `Proziceri_enriched.csv`

**Columns**:
- `id` - Unique identifier (1-890)
- `part_one` - First part of proverb
- `separator` - Connecting element
- `part_two` - Second part of proverb
- `category` - Thematic classification

### Example Entries

```csv
id,part_one,separator,part_two,category
1,Va răsări soarele,și,pe ulița noastră.,nature
5,A nu avea nici sfânt,""",""",nici Dumnezeu.,divine
23,A plecat plouă,dar,a venit frig.,nature
156,A vrut să se întrece cu sfântul,dar,nu-i ajung ouăle.,wisdom
```

## Categories

### 1. **Wisdom** (436 entries, 49.0%)
General wisdom, advice, and observations about life.

Examples:
- "Numai când moare omul,se cunoaște ce-a fost."
- "Cuvântul furat,e de aur."
- "Nu-i bine să ai secere în rând,fără să ai și bună vântul."

### 2. **Nature** (190 entries, 21.3%)
Animals, weather, seasons, and natural phenomena.

Examples:
- "Va răsări soarele,și,pe ulița noastră."
- "Cum scriu caii sub brazi,așa scriu și oamenii."
- "Când plouă și soarele strălucește,ploaia nu-i de mult."

### 3. **Work** (69 entries, 7.8%)
Labor, employment, trade, and craftsmanship.

Examples:
- "Munca nu-i rușine,ci leneșul."
- "Cine muncește cu plăcere,munceste cu ușurință."

### 4. **Love** (60 entries, 6.7%)
Relationships, marriage, attraction, and affection.

Examples:
- "Iubirea-ntâi,bogăția a doua."
- "Inima dragostei,și nu gura."

### 5. **Divine** (59 entries, 6.6%)
Religion, faith, divine providence, and morality.

Examples:
- "A nu avea nici sfânt,nici Dumnezeu."
- "Cine se-ncrede în Dumnezeu,nu cade în necaz."

### 6. **Death** (32 entries, 3.6%)
Mortality, fate, and the afterlife.

Examples:
- "Numai când moare omul,se cunoaște ce-a fost."
- "Moartea nu moare,ci-ncepe a trăi."

### 7. **Social** (27 entries, 3.0%)
Society, people, interaction, and communication.

Examples:
- "Omul fără cuvântul,nu-i om."
- "Ce aude un om în gură,aude toată lumea."

### 8. **Hardship** (6 entries, 0.7%)
Suffering, pain, and difficulty.

### 9. **Wealth** (6 entries, 0.7%)
Money, poverty, richness, and commerce.

### 10. **Character** (5 entries, 0.6%)
Personal qualities, virtues, and vices.

## Using the Enriched CSV

### Import into Python

```python
import pandas as pd

# Read enriched CSV
df = pd.read_csv('Proziceri_enriched.csv')

# Access data
print(df.shape)  # (890, 5)
print(df.columns)  # Index(['id', 'part_one', 'separator', 'part_two', 'category'])

# Filter by category
nature_proverbs = df[df['category'] == 'nature']
print(f"Found {len(nature_proverbs)} nature proverbs")

# Group statistics
print(df['category'].value_counts())
```

### Import into SQL Database

```python
import sqlite3
import pandas as pd

df = pd.read_csv('Proziceri_enriched.csv')
conn = sqlite3.connect('proverbs.db')

# Create table
df.to_sql('proverbs', conn, if_exists='replace', index=False)

# Query
cursor = conn.cursor()
cursor.execute("""
    SELECT * FROM proverbs
    WHERE category = 'love'
    LIMIT 5
""")
```

### Search by Category

```python
import csv

category_to_find = 'wisdom'

with open('Proziceri_enriched.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['category'] == category_to_find:
            print(f"[{row['id']}] {row['part_one']} {row['separator']} {row['part_two']}")
```

### Export to JSON

```python
import pandas as pd
import json

df = pd.read_csv('Proziceri_enriched.csv')

# Convert to JSON
data = df.to_dict(orient='records')

with open('proverbs.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## Category Assignment Methodology

Categories are assigned using **keyword-based heuristic matching**:

1. **Scan proverb text** for keywords associated with each category
2. **Count matches** across all categories
3. **Select category** with highest keyword match count
4. **Default to 'wisdom'** if no clear category match

### Example

Proverb: "Va răsări soarele,și,pe ulița noastră."

Keywords found:
- `nature`: "soarele" (sun) - **1 match** ✓ Winner
- `wisdom`: None - 0 matches

**Result**: Category = `nature`

## Limitations & Future Improvements

### Current Limitations
- **Automatic categorization**: May misclassify some proverbs
- **Single category**: Each proverb has only one primary category
- **Keyword-based**: Limited to predefined keywords

### Future Enhancements
1. **Manual review**: Validate and refine categorizations
2. **Multiple categories**: Support multiple tags per proverb
3. **Sentiment analysis**: Add positive/negative/neutral ratings
4. **Difficulty levels**: Classify by complexity for learners
5. **Etymology**: Add historical origin information
6. **Translation**: Support multilingual versions
7. **Audio**: Add pronunciation recordings
8. **Context**: Include usage examples and explanations

## Quality Assurance

### Validation Tests
- ✅ All 890 entries have unique sequential IDs
- ✅ All entries have a valid category
- ✅ Original proverb data is preserved
- ✅ CSV format is RFC 4180 compliant
- ✅ UTF-8 encoding with Romanian characters

### Test Results
```
Test Suite: TestEnrichedCSVFile
Tests run: 8
Successes: 8 ✓
Failures: 0
Errors: 0
```

## Statistics

### Category Distribution

| Category | Count | Percentage | Examples |
|----------|-------|-----------|----------|
| Wisdom | 436 | 49.0% | "Cuvântul furat e de aur" |
| Nature | 190 | 21.3% | "Va răsări soarele..." |
| Work | 69 | 7.8% | "Munca nu-i rușine" |
| Love | 60 | 6.7% | "Iubirea-ntâi..." |
| Divine | 59 | 6.6% | "Cine se-ncrede în Dumnezeu..." |
| Death | 32 | 3.6% | "Numai când moare omul..." |
| Social | 27 | 3.0% | "Omul fără cuvântul..." |
| Hardship | 6 | 0.7% | Various |
| Wealth | 6 | 0.7% | Various |
| Character | 5 | 0.6% | Various |
| **Total** | **890** | **100.0%** | |

## File Details

- **Filename**: `Proziceri_enriched.csv`
- **Format**: CSV (RFC 4180 compliant)
- **Encoding**: UTF-8
- **Rows**: 890 data entries + 1 header
- **Columns**: 5
- **Size**: ~140 KB

## Regenerating the Enriched CSV

To regenerate the enriched CSV from the cleaned version:

```bash
python3 enrich_csv.py
```

Output:
```
Enriching Proziceri_clean.csv...
======================================================================
ENRICHMENT COMPLETE
======================================================================
Total entries enriched: 890

Category Distribution:
...
```

## Files

- `Proziceri_clean.csv` - Standardized proverbs (original format)
- `Proziceri_enriched.csv` - Enhanced with ID and category
- `enrich_csv.py` - Script to create enriched version
- `ENRICHMENT_GUIDE.md` - This file

## See Also

- [TEST_REPORT.md](TEST_REPORT.md) - Test coverage and validation
- [STANDARDIZATION_REPORT.md](STANDARDIZATION_REPORT.md) - Standardization details
- [CSV_IMPROVEMENTS.md](CSV_IMPROVEMENTS.md) - Original improvement analysis

---

**Last Updated**: 2025-02-24
**Status**: Production Ready ✅
