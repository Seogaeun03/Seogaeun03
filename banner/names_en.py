"""영문 이름 픽셀 글자 시안. 획 굵기는 시안마다 하나로 고정."""
import os
from PIL import Image, ImageDraw, ImageFont
import room
from names import G, soften, draw

HERE = os.path.dirname(os.path.abspath(__file__))


def letter(ch, T=3, W=12, H=16):
    g = G(); R = W - 1; B = H - 1; m = H // 2 - T // 2   # 가운데 가로획 윗줄
    if ch == "S":
        g.box(1, 0, R, T - 1); g.box(0, 1, T - 1, m); g.box(1, m, R - 1, m + T - 1)
        g.box(R - T + 1, m + 1, R, B - 1); g.box(0, B - T + 1, R - 1, B)
    elif ch == "E":
        g.box(0, 0, T - 1, B); g.box(0, 0, R, T - 1); g.box(0, m, R - 2, m + T - 1); g.box(0, B - T + 1, R, B)
    elif ch == "O":
        g.box(1, 0, R - 1, T - 1); g.box(1, B - T + 1, R - 1, B); g.box(0, 1, T - 1, B - 1); g.box(R - T + 1, 1, R, B - 1)
    elif ch == "G":
        g.box(1, 0, R, T - 1); g.box(0, 1, T - 1, B - 1); g.box(1, B - T + 1, R - 1, B)
        g.box(R - T + 1, m, R, B - 1); g.box(W // 2, m, R, m + T - 1)
    elif ch == "A":
        g.box(1, 0, R - 1, T - 1); g.box(0, 1, T - 1, B); g.box(R - T + 1, 1, R, B); g.box(0, m + 1, R, m + T)
    elif ch == "U":
        g.box(0, 0, T - 1, B - 1); g.box(R - T + 1, 0, R, B - 1); g.box(1, B - T + 1, R - 1, B)
    elif ch == "N":
        g.box(0, 0, T - 1, B); g.box(R - T + 1, 0, R, B)
        g.diag(T - 1, 0, (W - 2 * T + 1) * 2 - 1, 1, T, 2)
    return g, W


def word(text, T=3, W=12, H=16, gap=2, space=6):
    pts = set(); ox = 0
    for ch in text:
        if ch == " ":
            ox += space; continue
        g, w = letter(ch, T, W, H)
        pts |= g.shift(ox); ox += w + gap
    return soften(pts)


def stacked(a, b, **kw):
    p1 = word(a, **kw); p2 = word(b, **kw); H = kw.get("H", 16)
    return p1 | {(x, y + H + 4) for x, y in p2}


def galmuri_ko():
    f = ImageFont.truetype(os.path.join(HERE, "fonts", "Galmuri11-Bold.ttf"), 11)
    m = Image.new("L", (60, 16), 0); d = ImageDraw.Draw(m); d.fontmode = "1"
    d.text((1, 1), "서가은", font=f, fill=255)
    pts = {(x, y) for x in range(60) for y in range(16) if m.getpixel((x, y))}
    return {(x * 2 + dx, y * 2 + dy) for x, y in pts for dx in (0, 1) for dy in (0, 1)}


if __name__ == "__main__":
    room.TITLE = Image.new("L", (1, 1), 0)
    variants = [
        ("1", "SEO GAEUN 굵은 획", word("SEO GAEUN"), 0),
        ("2", "GAEUN SEO", word("GAEUN SEO"), 0),
        ("3", "두 줄 크게", stacked("SEO", "GAEUN", T=3, W=13, H=15, gap=3), 0),
        ("4", "가는 획 넓은 자간", word("SEO GAEUN", T=2, W=11, H=14, gap=3, space=8), 0),
        ("5", "참고: 한글 전문 픽셀 글꼴 2배", galmuri_ko(), 0),
    ]
    crops = []
    for key, name, pts, _ in variants:
        big = room.frame(5)
        im = big.resize((room.NW, room.NH), Image.NEAREST); px = im.load()
        h = max(y for _, y in pts) + 1
        y0 = 24 - h // 2 if h < 30 else 6
        draw(px, pts, 20, y0)
        out = im.resize((room.NW * room.SC, room.NH * room.SC), Image.NEAREST)
        out.save(os.path.join(HERE, f"name_en_{key}.png"))
        c = out.crop((0, 0, 760, 320))
        crops.append(c)
    sheet = Image.new("RGB", (760 * 2 + 20, 340 * 3), (255, 255, 255))
    for i, c in enumerate(crops):
        sheet.paste(c, ((i % 2) * 780, (i // 2) * 340))
    sheet.save(os.path.join(HERE, "name_en_options.png"))
    print("ok")
