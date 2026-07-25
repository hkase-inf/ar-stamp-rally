from PIL import Image

src = Image.open("grace-hopper-source.png").convert("RGBA")
w, h = src.size

# Crop to just the portrait (right-hand side), drop the name text / QR code
left = int(w * 0.52)
box = (left, 0, w, h)
portrait = src.crop(box)

# Trim surrounding pure-white margin so the sticker hugs the figure
pw, ph = portrait.size
px = portrait.load()

def row_has_ink(y):
    for x in range(0, pw, 4):
        r, g, b, a = px[x, y]
        if r < 245 or g < 245 or b < 245:
            return True
    return False

def col_has_ink(x):
    for y in range(0, ph, 4):
        r, g, b, a = px[x, y]
        if r < 245 or g < 245 or b < 245:
            return True
    return False

top = 0
while top < ph and not row_has_ink(top):
    top += 1
bottom = ph - 1
while bottom > top and not row_has_ink(bottom):
    bottom -= 1
leftx = 0
while leftx < pw and not col_has_ink(leftx):
    leftx += 1
rightx = pw - 1
while rightx > leftx and not col_has_ink(rightx):
    rightx -= 1

pad = 15
top = max(0, top - pad)
bottom = min(ph - 1, bottom + pad)
leftx = max(0, leftx - pad)
rightx = min(pw - 1, rightx + pad)

portrait = portrait.crop((leftx, top, rightx, bottom))
portrait = portrait.convert("RGBA")
data = portrait.getdata()

new_data = []
for r, g, b, a in data:
    if r > 235 and g > 235 and b > 235:
        new_data.append((r, g, b, 0))
    elif r > 200 and g > 200 and b > 200:
        # feather the edge between ink and white
        fade = int(255 * (255 - min(r, g, b)) / (255 - 200))
        new_data.append((r, g, b, min(255, fade)))
    else:
        new_data.append((r, g, b, 255))

portrait.putdata(new_data)

max_w = 900
if portrait.width > max_w:
    ratio = max_w / portrait.width
    portrait = portrait.resize((max_w, int(portrait.height * ratio)), Image.LANCZOS)

portrait.save("grace-hopper-cutout.png")
print("saved", portrait.size)
