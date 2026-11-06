# Batter N' Life: site source (do not deploy this branch)

This branch holds the master copy used to build batternlife.com. The live site is on `main`.

- `boutique.src.html`: the whole site in one file. Images are written as `@@name@@` placeholders that point to `img/name.jpg` (or `.png` for logos).
- `build.py`: `python3 build.py` makes `batter-n-life-boutique.html` (single-file preview with images embedded) and the WebP images.
- `deploy.py`: `python3 deploy.py "commit message" /path/to/main-checkout` writes every page (/, /story/, /bake/, /mom/, /favorites/, /orders/, /privacy/, /contact/), copies images, updates robots.txt and sitemap.xml, then commits and pushes `main`. Add `--nopush` to only write the files.

Requires Python 3 with Pillow.

## Adding a Baking Journal tip
1. Save the photo as `img/note_<short-name>.jpg`.
2. In `boutique.src.html`, copy one `<button class="note" ...>` card inside `<div class="notes">` and one matching `<dialog class="ndialog" id="note-...">` near the end of the file. Give both the next number (`data-note="n4"` / `id="note-n4"`, "Tip no. 04"), then update the title, excerpt, date, photo placeholder and body.
3. Run `build.py`, then `deploy.py`.
