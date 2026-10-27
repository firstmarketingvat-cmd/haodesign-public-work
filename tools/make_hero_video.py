"""하오디자인 공공기관 포트폴리오 페이지로 히어로 배경 영상 생성 (1920x1080, 24fps, 루프)."""
import os, subprocess, sys, math
from PIL import Image, ImageFilter, ImageDraw

W_DIR = r"E:\public-work\assets\works"
OUT_MP4 = r"E:\public-work\assets\hero.mp4"
OUT_POSTER = r"E:\public-work\assets\hero-poster.jpg"
FW, FH, FPS = 1920, 1080, 24
SCENE_SEC, FADE_SEC = 4.0, 1.0
SW, SH = int(FW * 1.12), int(FH * 1.12)  # 장면 캔버스 (줌/이동 여유)

def bg():
    im = Image.new("RGB", (SW, SH), "#0f2140")
    d = ImageDraw.Draw(im)
    for y in range(SH):  # 세로 그라데이션 navy → 진한 navy
        t = y / SH
        c = (int(15 + 12 * (1 - t)), int(33 + 20 * (1 - t)), int(64 + 38 * (1 - t)))
        d.line([(0, y), (SW, y)], fill=c)
    return im

def place(canvas, name, cx, cy, h, rot=0):
    im = Image.open(os.path.join(W_DIR, name)).convert("RGB")
    w = round(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    # 그림자
    pad = 60
    sh = Image.new("L", (w + pad * 2, h + pad * 2), 0)
    ImageDraw.Draw(sh).rectangle([pad, pad + 18, pad + w, pad + h + 18], fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    layer = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    layer.putalpha(sh)
    page = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    page.paste(im, (pad, pad))
    layer = Image.alpha_composite(layer, page)
    if rot:
        layer = layer.rotate(rot, resample=Image.BICUBIC, expand=True)
    canvas.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)

X, Y = SW / 2, SH / 2
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
    """t: 0~1 장면 진행도, k: 장면 번호(이동 방향 교차)"""
    z = 1.0 + 0.07 * t
    cw, ch = SW / z / 1.12 * 1.0, SH / z / 1.12
    dx = (1 if k % 2 == 0 else -1) * 60 * (t - 0.5)
    left = (SW - cw) / 2 + dx
    top = (SH - ch) / 2 - 20 * (t - 0.5)
    return scene.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((FW, FH), Image.BILINEAR)

def main():
    scenes = [build_scene(s) for s in SCENES]
    n = len(scenes)
    per = int(SCENE_SEC * FPS)
    fade = int(FADE_SEC * FPS)
    total = per * n
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{FW}x{FH}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-pix_fmt", "yuv420p",
                           "-movflags", "+faststart", "-an", OUT_MP4], stdin=subprocess.PIPE)
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
            cur.save(OUT_POSTER, quality=80)
        ff.stdin.write(cur.tobytes())
    ff.stdin.close()
    ff.wait()
    print("mp4 MB:", round(os.path.getsize(OUT_MP4) / 1e6, 2), "poster KB:", os.path.getsize(OUT_POSTER) // 1024)

main()
