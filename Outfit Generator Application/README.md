# Outfit Generator Application

A local Python/Tkinter wardrobe manager and random outfit generator.

## Run

1. Install Python 3.10 or newer.
2. From this folder, run `python -m pip install -r requirements.txt`.
3. Start with `python app.py`.

Wardrobe records and saved outfits persist in `data/wardrobe.json` and `data/outfits.json`. Uploaded photos are copied into `data/images/` so the wardrobe does not depend on the original files.

## Tests

Run `python -m unittest discover -s tests -v`.
