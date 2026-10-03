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
- `content/resources/`: the Resources landing page and all English/Spanish guides.
- `assets/design/resources.css`: resource cards, guide images, and document layouts.
- `assets/placeholders/`: three user-supplied photos reused as placeholders.

Run `python scripts/build_site.py` after editing templates or content. This uses only the Python standard library and regenerates the main site and Constellation. Run `node tests/security.cjs` to check local links, assets, and security invariants. Run `node tests/resources.cjs` to verify the transferred guide collection and its media.

The most recent season in the supplied content is 2024–25; it is presented as a featured season, not a claim about the current season. The reused photos are temporary replacements, not historical portraits or sponsor logos. Google Fonts and the original video/document embeds require an internet connection. No analytics are included.

## Constellation

The original recreation is at `/constellation/home.html` and includes 27 public pages, the star map, local images, and site search. Curiosity's Resources link now opens `/resources.html`, which links directly to 17 English guides and two Spanish guides beneath `/resources/`. Resources is the single landing page; categories and Spanish resources are sections on that page.

Run `node scripts/build.cjs` to rebuild both sites. This also finds Codex's bundled Python on Windows when `python` is not on PATH. Preview with the existing `node preview.cjs` server.

See [the Constellation editing guide](content/constellation/README.md) for content, images, map positions, new pages, and source-link limitations. Run `node tests/constellation.cjs` alongside the existing security checks.
