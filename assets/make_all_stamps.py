import os
import cv2
import numpy as np
from PIL import Image, ImageOps

SRC_DIR = r"C:\Users\kase0\Downloads\20260725GrateFigures\20251025偉人画像"

PEOPLE = [
    ("grace-hopper", "01GraceHopper/image/Grace_Hopper_in_the_1940s_posterization_contrast.png"),
    ("tim-berners-lee", "02TimBernersLee/Tim_Berners-Lee_2023-corp_posterized.png"),
    ("marvin-minsky", "03MarvinMinsky/Marvin_Minsky01.png"),
    ("alan-turing", "04AlanTuring/Alan_Turing_(1951)01.png"),
    ("claude-shannon", "05ClaudeShannon/Alan_Turing_(1951)01.png"),  # placeholder, wrong photo, see note
    ("john-von-neumann", "06JohnvonNeumann/JohnvonNeumann-LosAlamos01.png"),
    ("alan-kay", "07AlanKay/Alan_Kay_and_the_prototype_of_Dynabook,_pt._5_(3010032738)01.png"),
    ("jun-murai", "08JunMurai/Jun_Murai_on_Jan_16,_2020_01.png"),
    ("herbert-simon", "09HerbertASimon/Herbert_Simon,_RIT_NandE_Vol13Num11_1981_Mar19_Complete01.png"),
]

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

    # pick the largest detected face
    x, y, w, h = max(candidates, key=lambda b: b[2] * b[3])
    return x, y, w, h


def alpha_bbox_fallback(rgba_img):
    alpha = rgba_img.getchannel("A")
    w, h = rgba_img.size
    band = alpha.crop((0, 0, w, int(h * 0.45)))
    bbox = band.getbbox()
    if not bbox:
        bbox = alpha.getbbox()
    x0, y0, x1, y1 = bbox
    return x0, y0, x1 - x0, y1 - y0


def make_stamp(person_id, rel_path):
    src_path = os.path.join(SRC_DIR, rel_path)
    img = Image.open(src_path).convert("RGBA")
    W, H = img.size

    face = detect_face_box(img)
    if face is None:
        face = alpha_bbox_fallback(img)
    fx, fy, fw, fh = face

    cx = fx + fw / 2
    cy = fy + fh / 2

    side = int(max(fw, fh) * 2.3)
    left = int(cx - side / 2)
    top = int(cy - side * 0.42)  # keep more headroom above, some room below for neck/collar

    left = max(0, min(left, W - 1))
    top = max(0, min(top, H - 1))
    right = min(W, left + side)
    bottom = min(H, top + side)
    left = max(0, right - side)
    top = max(0, bottom - side)

    square = img.crop((left, top, right, bottom))

    gray = ImageOps.grayscale(square)
    colorized = ImageOps.colorize(gray, black="#5c0f0a", white="#f3d9d2", mid="#b02a1e").convert("RGBA")
    colorized.putalpha(square.getchannel("A"))

    max_size = 640
    if colorized.width > max_size:
        colorized = colorized.resize((max_size, max_size), Image.LANCZOS)

    out_path = f"{person_id}-stamp.png"
    colorized.save(out_path)
    print(f"{person_id}: face_box={face} crop=({left},{top},{right},{bottom}) -> {out_path}")


if __name__ == "__main__":
    for person_id, rel_path in PEOPLE:
        make_stamp(person_id, rel_path)
