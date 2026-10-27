import fitz, os, io, sys
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image

SRC = r"C:\Users\ADMIN\Downloads\공공기관"
OUT = r"E:\public-work\assets\works"
os.makedirs(OUT, exist_ok=True)

SLUG = {
    "한국공작기계협회": "komma",
    "한국토지주택공사": "lh",
    "국제로타리": "rotary",
    "대불자유무역지역": "daebul-fez",
    "한국공기청정협회": "kaca",
    "자동차손해배상진흥원": "kaib",
    "한국의료재단_4단": "kmf-leaflet",
    "한국의료재단_브로슈어": "kmf-brochure",
    "나노기술연구회": "nano",
}

def save(pix, path, width=1100):
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    img.save(path, "JPEG", quality=82, optimize=True, progressive=True)
    return img.size

for f in sorted(os.listdir(SRC)):
    if not f.lower().endswith(".pdf"):
        continue
    slug = next((v for k, v in SLUG.items() if k in f), None)
    doc = fitz.open(os.path.join(SRC, f))
    n = doc.page_count
    p0 = doc[0].rect
    picks = {"cover": 0, "inner": min(n - 1, max(1, n // 2))}
    sizes = {}
    for tag, idx in picks.items():
        page = doc[idx]
        zoom = 1600 / max(page.rect.width, page.rect.height)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        sizes[tag] = save(pix, os.path.join(OUT, f"{slug}-{tag}.jpg"))
    print(f"{slug:13s} pages={n:2d} page0={p0.width:.0f}x{p0.height:.0f}pt cover={sizes['cover']} inner(p{picks['inner']+1})={sizes['inner']}  <- {f}")
