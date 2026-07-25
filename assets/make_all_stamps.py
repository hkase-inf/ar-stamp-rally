import os
import cv2
import numpy as np
from PIL import Image, ImageOps

SRC_DIR = r"C:\Users\kase0\Downloads\20260725GrateFigures\20251025偉人画像"

# (person_id, relative source path, manual face box override or None)
PEOPLE = [
    ("grace-hopper", "01GraceHopper/image/Grace_Hopper_in_the_1940s_posterization_contrast.png", None),
    ("tim-berners-lee", "02TimBernersLee/Tim_Berners-Lee_2023-corp_posterized.png", None),
    ("marvin-minsky", "03MarvinMinsky/Marvin_Minsky01.png", None),
    ("alan-turing", "04AlanTuring/Alan_Turing_(1951)01.png", None),
    ("claude-shannon", "05ClaudeShannon/C.E._Shannon._Tekniska_museet_43069_01.png", None),
    ("john-von-neumann", "06JohnvonNeumann/JohnvonNeumann-LosAlamos01.png", None),
    ("alan-kay", "07AlanKay/Alan_Kay_and_the_prototype_of_Dynabook,_pt._5_(3010032738)01.png", (1050, 400, 2020, 1370)),
    ("jun-murai", "08JunMurai/Jun_Murai_on_Jan_16,_2020_01.png", (600, 100, 1300, 800)),
    ("herbert-simon", "09HerbertASimon/Herbert_Simon,_RIT_NandE_Vol13Num11_1981_Mar19_Complete01.png", None),
]

# duotone (shadow, mid, highlight) per person -- distinct ink colors, not all red
COLORS = {
    "grace-hopper":     ("#5c0f0a", "#b02a1e", "#f3d9d2"),  # red
    "tim-berners-lee":  ("#0a2a5c", "#1e5ab0", "#d2e3f3"),  # blue
    "marvin-minsky":    ("#3a0a5c", "#6a1eb0", "#e3d2f3"),  # purple
    "alan-turing":      ("#0a5c4e", "#1eb094", "#d2f3ec"),  # teal
    "claude-shannon":   ("#5c330a", "#b0731e", "#f3e4d2"),  # orange
    "john-von-neumann": ("#16105c", "#3325b0", "#dcd8f3"),  # indigo
    "alan-kay":         ("#5c0a3d", "#b01e73", "#f3d2e6"),  # magenta
    "jun-murai":        ("#1a4d10", "#3d941e", "#dcf0d2"),  # green
    "herbert-simon":    ("#4a2f0a", "#8f631e", "#ecdfc9"),  # amber/brown
}

frontal = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
profile = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")


def detect_face_box(rgba_img):
    rgb = Image.alpha_composite(Image.new("RGBA", rgba_img.size, (255, 255, 255, 255)), rgba_img).convert("RGB")
    arr = np.array(rgb)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    candidates = []
    for scaleFactor in (1.05, 1.1, 1.2):
        faces = frontal.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5, minSize=(60, 60))
        candidates.extend(faces)
    if len(candidates) == 0:
        faces = profile.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        candidates.extend(faces)
        flipped = cv2.flip(gray, 1)
        faces_f = profile.detectMultiScale(flipped, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        w = gray.shape[1]
        for (x, y, fw, fh) in faces_f:
            candidates.append((w - x - fw, y, fw, fh))

    if not candidates:
        return None
    x, y, w, h = max(candidates, key=lambda b: b[2] * b[3])
    return int(x), int(y), int(w), int(h)


def alpha_bbox_fallback(rgba_img):
    alpha = rgba_img.getchannel("A")
    w, h = rgba_img.size
    band = alpha.crop((0, 0, w, int(h * 0.45)))
    bbox = band.getbbox()
    if not bbox:
        bbox = alpha.getbbox()
    x0, y0, x1, y1 = bbox
    return x0, y0, x1 - x0, y1 - y0


def make_stamp(person_id, rel_path, manual_box=None):
    src_path = os.path.join(SRC_DIR, rel_path)
    img = Image.open(src_path).convert("RGBA")
    W, H = img.size

    if manual_box:
        left, top, right, bottom = manual_box
    else:
        face = detect_face_box(img) or alpha_bbox_fallback(img)
        fx, fy, fw, fh = face
        cx = fx + fw / 2
        cy = fy + fh / 2
        side = int(max(fw, fh) * 2.3)
        left = int(cx - side / 2)
        top = int(cy - side * 0.42)
        right = left + side
        bottom = top + side

    # Crop with out-of-bounds coords allowed: PIL pads RGBA overflow with
    # transparent pixels, which keeps the square perfectly 1:1 (no stretch).
    square = img.crop((left, top, right, bottom))
    assert square.width == square.height, f"{person_id}: non-square crop {square.size}"

    gray = ImageOps.grayscale(square)
    black, mid, white = COLORS[person_id]
    colorized = ImageOps.colorize(gray, black=black, white=white, mid=mid).convert("RGBA")
    colorized.putalpha(square.getchannel("A"))

    max_size = 640
    if colorized.width != max_size:
        colorized = colorized.resize((max_size, max_size), Image.LANCZOS)

    out_path = f"{person_id}-stamp.png"
    colorized.save(out_path)
    print(f"{person_id}: crop=({left},{top},{right},{bottom}) size={square.size} -> {out_path}")


if __name__ == "__main__":
    for person_id, rel_path, manual_box in PEOPLE:
        make_stamp(person_id, rel_path, manual_box)
