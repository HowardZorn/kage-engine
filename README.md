# `kage-python`: A Python Implementation of Kage Engine

Kage Engine is a glyph generation engine for Chinese Characters (漢字、汉字), which is mainly developed by [@kamichikoichi](https://github.com/kamichikoichi/kage-engine) (上地宏一) and [@kurgm](https://github.com/kurgm/kage-engine). 

Based on @kurgm's nodejs implementation, this repository focuses on drawing Chinese character glyphs entirely with Bézier curves instead of the previous polygons.

# Example Usage

Firstly, You should download `dump_newest_only.txt` or `dump_all_versions.txt` from [GlyphWiki](https://glyphwiki.org/wiki/GlyphWiki:%e9%ab%98%e5%ba%a6%e3%81%aa%e6%b4%bb%e7%94%a8%e6%96%b9%e6%b3%95).

```python
from kage import Kage
from kage.font.sans import Sans
from kage.font.serif import Serif
import csv
import os
import multiprocessing

# Set the flag `ignore_component_version` if you want to use the glyph data in `dump_newest_only.txt`.
# This is because `dump_newest_only.txt` only contains the latest version of components.
# However, glyphs in `dump_newest_only.txt` may reference older versions of multiple components.
k = Kage(ignore_component_version=True)
# You can use `Serif()` as well!
k.font = Sans()

# generate a glyph
def gen(i: int):
    key = f'u{i:x}'
    canvas = k.make_glyph(name=key)
    canvas.saveas(os.path.join('./output', f'{key}.svg'))

# read the glyph data
with open('dump_newest_only.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines = csv.reader(lines, delimiter='|')
for i, line in enumerate(lines):
    if i <= 1 or len(line) < 3:
        continue
    line = [i.strip() for i in line]

    k.components.push(line[0], line[2])

# parallel generation
if __name__ == '__main__':
    with multiprocessing.Pool(16) as pool:
        pool.map(gen, list([0x6708, 0x6c23, 0x6728, 0x9ed1, 0x6230])) 
        # or maybe you wanna generate the basic CJK Unified Ideographs:
        # range(0x4E00, 0x9FA5 + 1)
```

# Sample

<img src="https://github.com/HowardZorn/kage-engine/raw/dev/output/u5f71.svg" />

<img src="https://github.com/HowardZorn/kage-engine/raw/dev/output/u5f71_serif.svg">

u+5f71，“影”

# TODO

- Serif: Algorithms for drawing offset curves with variable displacement have not been designed.

- doc: Lack of Documentation.

# Scholarship Information

[Kamichi Koichi](https://github.com/kamichikoichi) wrote a paper about his Kage Engine:

- Koichi KAMICHI (上地 宏一), KAGE - An Automatic Glyph Generating Engine For Large Character Code Set, 「書体・組版ワークショップ報告書」, pp.85-92, Glyph and Typesetting Workshop(書体・組版ワークショップ 京都大學21世紀COE 東アジア世界の人文情報學研究教育據點), 2003年11月28-29日, 京都大学人文科学研究所.