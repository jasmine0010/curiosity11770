# Curiosity 11770

Static robotics team website. No framework, package install, or third-party JavaScript is required.

## Preview

Run `node preview.cjs` and open `http://127.0.0.1:8765/home.html`.
The server supports both saved `.html` pages and the original extensionless routes.

## Edit

- `assets/design/site.css`: shared visual design and responsive layouts.
- `assets/design/site.js`: accessible mobile navigation.
- `scripts/build_site.py`: shared page layout and static page generation.
- `content/home.html`: homepage copy, photos, and slideshow markup.
- `content/pages.json`: the existing site's extracted editorial content.
- `assets/placeholders/`: three user-supplied photos reused as placeholders.

Run `python scripts/build_site.py` after editing templates or content. This uses only the Python standard library and regenerates all 36 HTML pages. Run `node tests/security.cjs` to check local links, assets, and security invariants.

The most recent season in the supplied content is 2024–25; it is presented as a featured season, not a claim about the current season. The reused photos are temporary replacements, not historical portraits or sponsor logos. Google Fonts and the original video/document embeds require an internet connection. No analytics are included.
