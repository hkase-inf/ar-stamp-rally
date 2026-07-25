from PIL import Image, ImageOps

src = Image.open("grace-hopper-photo-rgba.png").convert("RGBA")
w, h = src.size
alpha = src.getchannel("A")

# Find the face/head region: scan the top ~45% of the image (avoids the
# hands/shoulders which are wider and lower) for the alpha bounding box.
band_h = int(h * 0.45)
band_alpha = alpha.crop((0, 0, w, band_h))
bbox = band_alpha.getbbox()
x0, y0, x1, y1 = bbox
face_cx = (x0 + x1) // 2

# Square crop centered on the face, extended down a bit for neck/collar
side = int((x1 - x0) * 1.55)
top = max(0, y0 - int(side * 0.08))
left = max(0, face_cx - side // 2)
right = min(w, left + side)
left = max(0, right - side)
bottom = min(h, top + side)

square = src.crop((left, top, right, bottom))

# Colorize: turn the grayscale posterization into a red "ink stamp" duotone
gray = ImageOps.grayscale(square)
colorized = ImageOps.colorize(gray, black="#5c0f0a", white="#f3d9d2", mid="#b02a1e")
colorized = colorized.convert("RGBA")
colorized.putalpha(square.getchannel("A"))

max_size = 640
if colorized.width > max_size:
    colorized = colorized.resize((max_size, max_size), Image.LANCZOS)

colorized.save("grace-hopper-stamp.png")
print("saved", colorized.size, "crop box", (left, top, right, bottom))
