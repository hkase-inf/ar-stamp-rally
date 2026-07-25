import os
from PIL import Image, ImageOps

SRC_DIR = r"C:\Users\kase0\Downloads\20260725GrateFigures\20251025偉人画像"

OVERRIDES = [
    ("alan-kay", "07AlanKay/Alan_Kay_and_the_prototype_of_Dynabook,_pt._5_(3010032738)01.png",
     (1050, 400, 2020, 1370)),
    ("jun-murai", "08JunMurai/Jun_Murai_on_Jan_16,_2020_01.png",
     (600, 100, 1300, 800)),
]


def make_stamp(person_id, rel_path, box):
    src_path = os.path.join(SRC_DIR, rel_path)
    img = Image.open(src_path).convert("RGBA")
    square = img.crop(box)

    gray = ImageOps.grayscale(square)
    colorized = ImageOps.colorize(gray, black="#5c0f0a", white="#f3d9d2", mid="#b02a1e").convert("RGBA")
    colorized.putalpha(square.getchannel("A"))

    max_size = 640
    if colorized.width > max_size:
        ratio = max_size / colorized.width
        colorized = colorized.resize((max_size, int(colorized.height * ratio)), Image.LANCZOS)

    out_path = f"{person_id}-stamp.png"
    colorized.save(out_path)
    print(f"{person_id}: crop={box} -> {out_path} size={colorized.size}")


if __name__ == "__main__":
    for person_id, rel_path, box in OVERRIDES:
        make_stamp(person_id, rel_path, box)
