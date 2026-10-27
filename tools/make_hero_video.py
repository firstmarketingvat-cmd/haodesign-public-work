"""하오디자인 공공기관 포트폴리오 페이지로 히어로 배경 영상 생성 (1920x1080, 24fps, 루프).

선명도를 위해
- 원본 PDF가 있으면(PDF_DIR) 페이지를 필요한 크기 그대로 PDF에서 직접 렌더링 (없으면 assets/works JPG 사용)
- 장면을 2배 해상도(SS)로 만든 뒤 프레임마다 축소(다운샘플)
- 높은 화질(CRF 23)로 인코딩
"""
import os, subprocess, sys, io
from PIL import Image, ImageFilter, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W_DIR = os.path.join(ROOT, "assets", "works")
OUT_MP4 = os.path.join(ROOT, "assets", "hero.mp4")
OUT_POSTER = os.path.join(ROOT, "assets", "hero-poster.jpg")
PDF_DIR = r"C:\Users\ADMIN\Downloads\공공기관"   # 원본 PDF 폴더 (없으면 JPG로 대체)
PDF_KEY = {  # 슬러그 → PDF 파일명 일부 (tools/render_pdfs.py 와 같은 규칙)
    "komma": "한국공작기계협회", "lh": "한국토지주택공사", "rotary": "국제로타리",
    "daebul-fez": "대불자유무역지역", "kaca": "한국공기청정협회", "kaib": "자동차손해배상진흥원",
    "kmf-leaflet": "한국의료재단_4단", "kmf-brochure": "한국의료재단_브로슈어", "nano": "나노기술연구회",
}
FW, FH, FPS = 1920, 1080, 24
SS = 2                                   # 슈퍼샘플링 배율
SCENE_SEC, FADE_SEC = 4.0, 1.0
SW, SH = int(FW * 1.12 * SS), int(FH * 1.12 * SS)   # 장면 캔버스 (줌/이동 여유 포함)

def bg():
    im = Image.new("RGB", (SW, SH), "#0e1b2c")
    d = ImageDraw.Draw(im)
    for y in range(SH):  # 세로 그라데이션: 네이비 #1F3450(위) → 미드나잇 #0E1B2C(아래)
        t = y / SH
        c = (int(14 + 17 * (1 - t)), int(27 + 25 * (1 - t)), int(44 + 36 * (1 - t)))
        d.line([(0, y), (SW, y)], fill=c)
    # 오른쪽 위 하오 버밀리언 빛 번짐(아주 은은하게)
    glow = Image.new("L", (SW // 4, SH // 4), 0)
    ImageDraw.Draw(glow).ellipse([SW / 4 * .62, -SH / 4 * .35, SW / 4 * 1.25, SH / 4 * .55], fill=55)
    glow = glow.filter(ImageFilter.GaussianBlur(55)).resize((SW, SH), Image.BICUBIC)
    return Image.composite(Image.new("RGB", (SW, SH), "#e83817"), im, glow)

def load_page(name, h):
    """name 예: 'lh-inner.jpg' → 높이 h(px)짜리 페이지 이미지. PDF가 있으면 PDF에서 바로 렌더."""
    slug, tag = name[:-4].rsplit("-", 1)
    try:
        import fitz
        pdf = next(f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf") and PDF_KEY[slug] in f)
        doc = fitz.open(os.path.join(PDF_DIR, pdf))
        idx = 0 if tag == "cover" else min(doc.page_count - 1, max(1, doc.page_count // 2))
        page = doc[idx]
        zoom = h * 1.5 / page.rect.height          # 1.5배로 렌더 후 축소 → 글자 안티앨리어싱
        im = Image.open(io.BytesIO(page.get_pixmap(matrix=fitz.Matrix(zoom, zoom)).tobytes("png"))).convert("RGB")
    except Exception:
        im = Image.open(os.path.join(W_DIR, name)).convert("RGB")
    w = round(im.width * h / im.height)
    return im.resize((w, h), Image.LANCZOS)

def place(canvas, name, cx, cy, h, rot=0):
    cx, cy, h = cx * SS, cy * SS, int(h * SS)
    im = load_page(name, h)
    w = im.width
    pad = 60 * SS
    sh = Image.new("L", (w + pad * 2, h + pad * 2), 0)
    ImageDraw.Draw(sh).rectangle([pad, pad + 18 * SS, pad + w, pad + h + 18 * SS], fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(26 * SS))
    layer = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    layer.putalpha(sh)
    page = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    page.paste(im, (pad, pad))
    layer = Image.alpha_composite(layer, page)
    if rot:
        layer = layer.rotate(rot, resample=Image.BICUBIC, expand=True)
    canvas.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)

X, Y = FW * 1.12 / 2, FH * 1.12 / 2      # 좌표·크기는 1배 기준으로 적고 place()에서 SS배
SCENES = [  # (파일, cx, cy, 높이, 회전)
    [("lh-cover.jpg", X - 470, Y + 10, 640, 3), ("lh-inner.jpg", X + 420, Y - 20, 700, -2)],
    [("kmf-brochure-cover.jpg", X - 560, Y, 760, 2), ("kmf-brochure-inner.jpg", X + 260, Y + 10, 660, -2)],
    [("nano-inner.jpg", X + 280, Y + 20, 700, -1.5), ("nano-cover.jpg", X - 430, Y - 30, 560, 2.5)],
    [("komma-cover.jpg", X - 560, Y, 760, 3), ("komma-inner.jpg", X - 40, Y + 20, 720, -1), ("kaca-cover.jpg", X + 560, Y - 10, 380, -3)],
    [("rotary-cover.jpg", X - 400, Y - 10, 660, 2), ("rotary-inner.jpg", X + 440, Y + 30, 600, -2.5)],
    [("daebul-fez-inner.jpg", X - 500, Y - 40, 520, 2), ("kaib-cover.jpg", X + 380, Y - 60, 540, -2), ("kmf-leaflet-inner.jpg", X - 40, Y + 260, 360, 1)],
]

def build_scene(items):
    c = bg()
    for it in items:
        place(c, *it)
    return c

def frame_of(scene, t, k):
    """t: 0~1 장면 진행도, k: 장면 번호(이동 방향 교차). 확대는 5%까지만(과한 확대 = 흐림)."""
    z = 1.0 + 0.05 * t
    cw, ch = SW / z / 1.12, SH / z / 1.12
    dx = (1 if k % 2 == 0 else -1) * 50 * SS * (t - 0.5)
    left = (SW - cw) / 2 + dx
    top = (SH - ch) / 2 - 16 * SS * (t - 0.5)
    return scene.resize((FW, FH), Image.LANCZOS, box=(left, top, left + cw, top + ch), reducing_gap=2.0)

def main():
    scenes = [build_scene(s) for s in SCENES]
    n = len(scenes)
    per = int(SCENE_SEC * FPS)
    fade = int(FADE_SEC * FPS)
    total = per * n
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{FW}x{FH}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "slow", "-tune", "stillimage", "-crf", "23",
                           "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", OUT_MP4], stdin=subprocess.PIPE)
    span = per + fade  # 각 장면이 보이는 전체 길이 (다음 장면과 겹치는 페이드 포함)
    for f in range(total):
        k = f // per
        local = f - k * per
        cur = frame_of(scenes[k], (local + fade) / span, k)
        if local >= per - fade:  # 다음 장면으로 페이드 (마지막은 첫 장면으로 → 루프)
            nk = (k + 1) % n
            nxt = frame_of(scenes[nk], (local - (per - fade)) / span, nk)
            a = (local - (per - fade)) / fade
            cur = Image.blend(cur, nxt, a * a * (3 - 2 * a))
        if f == fade:
            cur.save(OUT_POSTER, quality=85)
        ff.stdin.write(cur.tobytes())
    ff.stdin.close()
    ff.wait()
    print("mp4 MB:", round(os.path.getsize(OUT_MP4) / 1e6, 2), "poster KB:", os.path.getsize(OUT_POSTER) // 1024)

main()
