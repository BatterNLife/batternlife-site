# Batter N' Life: site source (do not deploy this branch)

This branch holds the master copy used to build batternlife.com. The live site is on `main`.

- `boutique.src.html`: the whole site in one file. Images are written as `@@name@@` placeholders that point to `img/name.jpg` (or `.png` for logos).
- `build.py`: `python3 build.py` makes `batter-n-life-boutique.html` (single-file preview with images embedded) and the WebP images.
- `deploy.py`: `python3 deploy.py "commit message" /path/to/main-checkout` writes every page (/, /story/, /bake/, /mom/, /favorites/, /orders/, /privacy/, /contact/), copies images, updates robots.txt and sitemap.xml, then commits and pushes `main`. Add `--nopush` to only write the files.

Requires Python 3 with Pillow.

## Adding a Baking Journal tip
1. Save the photo as `img/note_<short-name>.jpg`.
2. In `boutique.src.html`, copy one `<button class="note" ...>` card inside `<div class="notes">` and one matching `<dialog class="ndialog" id="note-...">` near the end of the file. Give both the next number (`data-note="n4"` / `id="note-n4"`, "Tip no. 04"), then update the title, excerpt, date, photo placeholder and body.
3. Entry order inside the dialog: date line, title, text, then `<p class="nd-sign">xo, Melinda</p>`, then (if there is a reel) the `<div class="nd-video">` block LAST. Videos ALWAYS go at the end of an entry, never in the middle. The previous/next tip arrows are added automatically by script. Cards with a reel get `<span class="note-vid">▶ Video</span>` after the tip number.
4. Run `build.py`, then `deploy.py`.

## Adding a Mom Diaries entry (Mom Life)
- Card: copy a `<button class="mnote" data-cat="life|school|fun|notes" data-note="mN">` inside `<div class="mnotes">`. Put the NEWEST entry FIRST (the first card is the big "Latest" one). Category label goes in `<span class="mn-type">`.
- Photo: add `<span class="mn-photo"><img src="@@img_name@@" alt=""></span>` before the `<h3>`. It only shows when that card is the big featured card. Also put the photo in the dialog's `<div class="nd-img">`.
- Dialog: `<dialog class="ndialog" id="note-mN">` with date line, `<h2>` title, paragraphs, `<h3>` subheads, then `<p class="nd-sign">xo, Melinda</p>`.
- Remove `<span class="mn-sample">Sample</span>` on real entries. Mom Life new sections are preview-only (class `pvmom`) until the samples are replaced.
