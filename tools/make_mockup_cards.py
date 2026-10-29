"""Drive 목업 PNG → 카드용 JPG (빈 배경을 잘라 인쇄물이 크게 보이도록, 280x199 카드 비율).
사용: python tools/make_mockup_cards.py <PNG폴더> assets/works/mockup   (PNG 이름은 tools/mockup_sources.txt 의 '슬러그_번호')
PNG폴더에 없으면 '<PNG폴더>2' 에서도 찾습니다."""
import sys, os
from PIL import Image, ImageChops
src, dst = sys.argv[1], sys.argv[2]
PICK = {'btp':'btp_3','csia':'csia_1','daegu':'daegu_thum','foodsafety':'foodsafety_2','gangnam':'gangnam_2',
        'goryeong':'goryeong_thum','kead':'kead_1','kepco':'kepco_1','kicet':'kicet_1','kipi':'kipi_1','kist':'kist_1',
        'koipa':'koipa_1','regen':'regen_1','sen':'sen_thum','seocho':'seocho_thum','snuh':'snuh_1','komma':'komma_2'}
R = 280 / 199
os.makedirs(dst, exist_ok=True)
for slug, name in PICK.items():
    p = os.path.join(src, name + '.png')
    if not os.path.exists(p): p = os.path.join(src + '2', name + '.png')
    im = Image.open(p).convert('RGB'); W, H = im.size
    bg = Image.new('RGB', im.size, im.getpixel((5, 5)))
    diff = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 28 else 0)
    l, t, r, b = diff.getbbox() or (0, 0, W, H)
    pad = 0.06 * max(r - l, b - t); l, t, r, b = l - pad, t - pad, r + pad, b + pad
    w, h = r - l, b - t
    if w / h < R: w = h * R
    else: h = w / R
    w, h = min(w, W, H * R), min(h, H, W / R)
    cx, cy = (l + r) / 2, (t + b) / 2
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    out = im.crop((round(x0), round(y0), round(x0 + w), round(y0 + h))).resize((840, 597), Image.LANCZOS)
    out.save(os.path.join(dst, slug + '-mock.jpg'), quality=82, optimize=True, progressive=True)
    print(slug, name, os.path.getsize(os.path.join(dst, slug + '-mock.jpg')) // 1024, 'KB')
