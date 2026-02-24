# Deployment Guide

## Current Structure

The website files live at the project root alongside `data/` and other directories:

```
proziceri/
├── index.html      ← Main entry point
├── proziceri.js    ← Core logic
├── proziceri.css   ← Styling
├── data/           ← CSV data files
├── tests/          ← Test files (development only)
└── ...
```

## Deployment Options

### Option 1: Simple Web Server
Configure your web server root to serve from the project root. All paths are relative:
- Website files: `*.html`, `*.js`, `*.css` at root
- Data files: `data/Proziceri.csv`

### Option 2: CDN Deployment
- Deploy the project root to your main server
- Deploy `data/Proziceri.csv` to a CDN
- Update `proziceri.js` line 112 to point to CDN URL

## File Paths

The website expects:
- CSS/JS: Same directory as `index.html` (project root)
- CSV Data: `data/Proziceri.csv` (relative to project root)

## Web Server Configuration

### Apache (.htaccess)
If the site is served from the project root, ensure `.htaccess` allows directory browsing and CORS if needed.

### Nginx
Configure to serve from project root with proper MIME types for CSV.

### Python (Development)
```bash
# From project root, serve all files
python3 -m http.server 8000
# Access at http://localhost:8000/
```

## Important Notes

1. **CORS**: If CSV is on a different domain, ensure CORS headers are set
2. **File Paths**: The CSV loader uses a relative path (`data/Proziceri.csv`)
3. **CSV Format**: Ensure UTF-8 encoding maintained in transit
4. **Caching**: CSV files can be cached; consider cache busting for updates

## Testing Deployment

After deploying, verify:
```javascript
// Open browser console and check:
- Network tab: Should load data/Proziceri.csv successfully
- Console: No 404 errors for CSS, JS, or CSV
- Functionality: Click "meșterește una nouă" should generate sayings
```

## Rollback Plan

If issues occur:
1. Revert `proziceri.js` line 112 to hardcoded path if needed
2. All tools in `tools/` are development-only and don't affect live site
