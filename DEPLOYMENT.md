# Deployment Guide

## Current Structure (Post-Reorganization)

The project is now organized into logical folders:

```
proziceri/
├── website/        ← Serve this folder to users
├── data/           ← CSV data files (must be accessible to website)
├── tools/          ← Development tools only
├── tests/          ← Test files (development only)
└── docs/           ← Documentation
```

## Deployment Options

### Option 1: Simple Web Server (All-in-one)
If deploying the entire project, configure your web server root to serve from the project root:
- Website files: `website/*`
- Data files: `data/*` (accessible as `/data/Proziceri.csv`)

### Option 2: Separate Deployment
Deploy only what users need:
1. Copy `website/` folder → `/var/www/proziceri/`
2. Copy `data/` folder → `/var/www/proziceri/data/`
3. Configure web server to serve from `/var/www/proziceri/`

### Option 3: CDN Deployment
- Deploy `website/` to your main server
- Deploy `data/Proziceri.csv` to a CDN
- Update `website/proziceri.js` line 112 to point to CDN URL

## File Paths

The website expects:
- CSS/JS: Same directory as `index.html` (all in `website/`)
- CSV Data: `../data/Proziceri.csv` (relative to `website/` folder)

## Web Server Configuration

### Apache (.htaccess)
If the site is served from the project root, ensure `.htaccess` allows directory browsing and CORS if needed.

### Nginx
Configure to serve from project root with proper MIME types for CSV.

### Python (Development)
```bash
# From project root, serve all files
python3 -m http.server 8000
# Access at http://localhost:8000/website/
```

Or serve just the website:
```bash
cd website
python3 -m http.server 8000
# Then update proziceri.js to load from /data/Proziceri.csv
# (This requires data folder to be accessible)
```

## Important Notes

1. **CORS**: If CSV is on a different domain, ensure CORS headers are set
2. **File Paths**: The CSV loader uses relative paths (`../data/Proziceri.csv`)
3. **CSV Format**: Ensure UTF-8 encoding maintained in transit
4. **Caching**: CSV files can be cached; consider cache busting for updates

## Testing Deployment

After deploying, verify:
```javascript
// Open browser console and check:
- Network tab: Should load ../data/Proziceri.csv successfully
- Console: No 404 errors for CSS, JS, or CSV
- Functionality: Click "meșterește una nouă" should generate sayings
```

## Rollback Plan

If issues occur:
1. Revert `website/proziceri.js` line 112 to hardcoded path if needed
2. All tools in `tools/` are development-only and don't affect live site
