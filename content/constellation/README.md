# Editing Constellation

Constellation is the Curiosity site's editable resource branch. The 27 pages share a dark editorial design, while the homepage keeps its interactive star map. All lasting edits belong in `content/constellation/` or `assets/constellation/`; generated pages under `constellation/` are replaced by every build.

## Build and preview

From the project root, run:

```sh
node scripts/build.cjs
node preview.cjs
```

Open **http://127.0.0.1:8765/constellation/home.html**. If preview is already running, rebuild and refresh. The build also regenerates Curiosity's pages and does not change their source files. To validate, run `node tests/constellation.cjs` and `node tests/security.cjs`.

## Edit a resource page

Open the matching file in `content/constellation/pages/`. For example, `pages/north-star-resources/cnc-guide.html` holds the CNC guide. Each file contains simple editable `<section>` elements with `.c-content-grid` and `.c-column` wrappers. Edit text inside headings, paragraphs, lists, and links; copy a nearby section when adding more content. Use `<h2>` for major headings and `<h3>` below them. The shared page masthead supplies the single `<h1>` automatically from `pages.json`.

To change a page's navigation title or masthead image, edit its `title` or `heroImage` in `pages.json`. An optional `heading` keeps the original page heading when it differs from the navigation title; `null` keeps the masthead graphic without adding a visible heading to pages that originally had none. Put new images in `assets/constellation/`, then reference them with root-relative paths such as `/assets/constellation/example.jpg`. Add meaningful `alt` text when the image carries information; use `alt=""` when nearby text already names the same resource. `asset-manifest.json` maps imported image URLs to local files.

The layouts respond to their content: a single text column stays wide, text with photos forms an editorial grid, resource cards form a directory, and `.c-embed` frames documents or videos. Edit shared colors, type, spacing, cards, navigation, and footer styles in `assets/constellation/site.css`; edit the footer's links and copy in `footer.html`. Constellation deliberately uses Curiosity's Archivo type, near-black surfaces, cream text, deep red, and a distinct amber accent. It does not depend on the exported Google Sites CSS.

An external document or video has a sandboxed `<iframe>` plus a direct-open `.c-action` link. Update both URLs together and keep the iframe `title` and `sandbox` attributes. External services still require internet access and may refuse embedding; the direct link remains usable.

## Edit the star map

`map.json` contains the six stars' labels, local destinations, IDs, designations, positions, and connections. Connections refer to the numeric suffix of each star ID; `[5, 1]` connects North Star to Comets. Edit a star's `position` custom properties (`--x`, `--y`, `--mx`, `--my`) for desktop and mobile placement. The `fieldStars` array holds the fixed minor stars; each has percentage coordinates, a `micro` or `minor` size, and a `cool`, `neutral`, or `warm` tone. The two `comets` have percentage start coordinates, a travel angle in degrees, a travel distance in pixels, and a slow duration in seconds. Their tails rotate with their travel path. The mobile destination list is generated from the same six links. `assets/constellation/map.css` controls the plate's colors, star hierarchy, hairline connections, firework particles, and annotation layout; `assets/constellation/chart-grid.svg` holds the faint coordinate grid. `assets/constellation/site.js` controls search, navigation, connection geometry, the motion toggle, and star-hover fireworks. Rebuild and check desktop and phone sizes after moving a star.

## Add a page

1. Copy a similar page fragment into `content/constellation/pages/` using the intended route as its filename, such as `north-star-resources/new-guide.html`. Do not add a header, footer, or `<h1>`.
2. Add its `slug`, `title`, and optional `heroImage` to `pages.json`.
3. Add a link from the relevant directory page. Subpages appear in the navigation dropdown and search index after building.
4. Rebuild and run both checks. `inventory.json` is a record of the original 27-page import; update the coverage expectation only if you intentionally change that snapshot.

## Existing external-resource limitations

The original team-pairing Google Form returned 404 during import. Some other external links returned 403 or a redirect loop in automated checks; they remain in place. The external FTC pairing application loaded as a blank page in the preview browser because of errors in its own scripts. Embedded documents could not all be visually verified inside the preview browser. `external-resources.json` records the 51 imported external destinations and their check results; `scripts/check_constellation_links.py` can recheck them. Search indexes local page text, not the contents of third-party documents. No publishing or domain setting is part of the build.
