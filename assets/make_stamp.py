from PIL import Image, ImageDraw, ImageOps

src = Image.open("grace-hopper-cutout.png").convert("RGBA")
w, h = src.size

# Face-centered square crop for a circular stamp badge
side = int(w * 0.92)
cx = int(w * 0.5)
top = int(h * 0.03)
box = (max(0, cx - side // 2), top, min(w, cx + side // 2), top + side)
square = src.crop(box)
square = square.resize((640, 640), Image.LANCZOS)

# Composite onto white so the circle reads as a solid ink stamp, not a cutout with holes
white_bg = Image.new("RGBA", square.size, (255, 255, 255, 255))
flat = Image.alpha_composite(white_bg, square)

# Desaturate + tint slightly toward a warm "ink" grey
gray = ImageOps.grayscale(flat).convert("RGBA")

mask = Image.new("L", gray.size, 0)
d = ImageDraw.Draw(mask)
pad = 6
d.ellipse((pad, pad, gray.width - pad, gray.height - pad), fill=255)

out = Image.new("RGBA", gray.size, (0, 0, 0, 0))
out.paste(gray, (0, 0), mask)

out.save("grace-hopper-stamp.png")
print("saved", out.size)
