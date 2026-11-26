"""Rebuild fonts/wenkai.woff2 from the characters used in index.html.

Run after changing any text on the page:
    python tools/subset-font.py [path/to/LXGWWenKai-Regular.ttf]

Needs: pip install fonttools brotli
"""

import pathlib
import string
import sys

from fontTools import subset

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "fonts" / "LXGWWenKai-Regular.ttf"
TARGET = ROOT / "fonts" / "wenkai.woff2"

text = (ROOT / "index.html").read_text(encoding="utf-8")
chars = set(text) | set(string.printable) | set("，。、；：？！“”‘’（）《》·—…")
chars = "".join(sorted(c for c in chars if not c.isspace() or c == " "))

options = subset.Options()
options.flavor = "woff2"
options.layout_features = ["*"]
options.name_IDs = ["*"]
options.notdef_outline = True

font = subset.load_font(str(SOURCE), options)
subsetter = subset.Subsetter(options)
subsetter.populate(text=chars)
subsetter.subset(font)
TARGET.parent.mkdir(exist_ok=True)
subset.save_font(font, str(TARGET), options)

print(f"{len(chars)} characters -> {TARGET.relative_to(ROOT)} ({TARGET.stat().st_size // 1024} KB)")
