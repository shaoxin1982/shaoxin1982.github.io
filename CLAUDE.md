# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static portfolio website generator that converts JSON data into professional HTML portfolio/resume pages using Jinja2 templating. The generator produces two outputs: a full portfolio page (`index.html`) and a print-optimized resume page (`resume.html`).

## Key Commands

### Generate Portfolio
```bash
python generate_portfolio.py
```
This reads `portfolio-simon.json`, loads social link SVG icons, and renders both `index.html` and `resume.html`.

### Development Environment
```bash
# Install dependencies using uv (preferred)
uv sync

# Or using pip
pip install -r requirements.txt
```

Python version: 3.13 (specified in `.python-version`)

## Architecture

### Data Flow
```
portfolio-simon.json → generate_portfolio.py → Jinja2 Templates → HTML Output
```

1. **Input**: `portfolio-simon.json` contains all portfolio data (personal info, work experience, projects, education, skills, certifications)
2. **Processing**: `generate_portfolio.py` loads the JSON, dynamically embeds SVG icons for social links, and adds current year
3. **Templating**: Two Jinja2 templates render the data:
   - `index_template.html` - Full portfolio with projects, interests, galleries
   - `resume_template.html` - Simplified, print-friendly version
4. **Output**: Static HTML files ready for deployment

### Important Implementation Details

**SVG Icon Embedding**: Social link icons (in `img/` directory) are loaded at build time and embedded inline in the HTML. This happens in `generate_portfolio.py` lines 14-18:
```python
for link in data["social_links"]:
    if link.get("svg_path"):
        with Path(link["svg_path"]).open(encoding="utf-8") as svg_file:
            link["svg_data"] = svg_file.read()
```

**Template Context**: Both templates receive the same data dictionary, allowing conditional rendering based on what fields are present in the JSON.

**Hardcoded Input**: The generator currently hardcodes `portfolio-simon.json` as input (line 8). To use different portfolio data, either:
- Modify the filename in the script
- Create a new JSON file following the same schema as `portfolio-corey.json` or `portfolio-simon.json`

## JSON Schema

Portfolio JSON files should include:
- `name`, `label`, `image_path`, `contact`, `summary`, `url`
- `social_links[]` - with `label`, `url`, `svg_path` (path to icon in `img/`)
- `work_experience[]` - company, position, dates, summary, highlights
- `projects[]` - title, summary, url, highlights, images (optional galleries)
- `education[]` - institution, location, degrees, honors, GPA, graduation date
- `skills[]` - name, proficiency (0-100), proficiency_label
- `certifications[]` - name, issuer, date
- `volunteer_experience[]`, `interests[]`, `languages[]`, `references[]` (all optional)

See `portfolio-corey.json` or `portfolio-simon.json` for complete examples.

## File Organization

- **Templates**: `index_template.html`, `resume_template.html`
- **Styles**: `css/main.css` (portfolio), `css/resume.css` (print styles)
- **Assets**: `img/` (social icons), `portfolio_media/` (profile photos, project images)
- **Data**: `portfolio-*.json` files
- **Output**: `index.html`, `resume.html` (generated, should not be edited directly)

## Common Modifications

### Adding a New Portfolio
1. Create `portfolio-{name}.json` following the existing schema
2. Update line 8 in `generate_portfolio.py` to reference the new file
3. Run `python generate_portfolio.py`
4. Add actual images to `portfolio_media/` directory

### Adding New Social Links
1. Add SVG icon to `img/` directory (18+ platforms already included)
2. Add entry to `social_links` array in portfolio JSON
3. Generator will automatically embed the SVG

### Customizing Templates
Edit `index_template.html` or `resume_template.html` directly. Changes take effect on next generation. Templates use Jinja2 syntax with autoescape enabled for security.

### Styling Changes
- Portfolio appearance: `css/main.css`
- Print/resume styles: `css/resume.css`
- Base styles: `css/modern_normalize.css`, `css/html5bp.css`

## Notes

- `main.py` is unused boilerplate and can be ignored
- `js/app.js` is minimal/empty - portfolio is primarily static
- Generated HTML files are production-ready for static hosting (GitHub Pages, Netlify, Vercel, etc.)
- PWA support included via `site.webmanifest` and icon files
- Templates are already responsive and print-friendly
