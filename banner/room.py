"""깃허브 프로필 배너 2차: 밤에 책상에서 도트를 찍는 방 장면.
원판 320x80 에서 그리고 4배(1280x320)로 키운다. 반 픽셀, 섞인 배율 없음."""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "Galmuri11.ttf")
FONTB = os.path.join(HERE, "fonts", "Galmuri11-Bold.ttf")
NW, NH, SC = 320, 80, 4

def hx(s):
    s = s.lstrip("#"); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)

C = {
    "k": hx("14121f"),           # 먹
    "w0": hx("1a1d38"), "w1": hx("212548"), "w2": hx("2a2f5a"),   # 벽
    "fl": hx("12142a"), "fl2": hx("1a1d38"),
    "sky": hx("0d1030"), "sky2": hx("161a45"), "star": hx("ffffff"), "star2": hx("8f9bff"),
    "moon": hx("fff2b8"), "frame": hx("3b4275"), "frameL": hx("525a96"),
    "wood": hx("8c4f3b"), "woodL": hx("b86a4c"), "woodD": hx("5c3127"),
    "scr": hx("7fe3ff"), "scrD": hx("2fa8d8"), "bez": hx("2a2d40"), "bezL": hx("454a66"),
    "pink": hx("ff5d8f"), "pinkD": hx("c63a70"), "pinkL": hx("ff9cbc"),
    "hair": hx("2c1d33"), "hairL": hx("5a3a5e"), "rim": hx("7fe3ff"),
    "skin": hx("ffd6bf"), "skinD": hx("e89a86"),
    "pant": hx("8fb3ff"), "pantD": hx("5f86e0"),
    "chair": hx("3a3f63"), "chairL": hx("525a8a"),
    "lamp": hx("ffcf4a"), "lampD": hx("d99a1e"), "glow": hx("ffe08a"),
    "cat": hx("f2f2f6"), "catD": hx("b8bad0"), "catE": hx("ff9cbc"),
    "mug": hx("2fd3a0"), "mugD": hx("1b9874"), "steam": hx("8a90c0"),
    "txt": hx("ffffff"), "sub": hx("a9b1ff"), "heart": hx("ff5d8f"),
}

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

def put(px, x, y, c):
    if 0 <= x < NW and 0 <= y < NH:
        px[x, y] = c

def rect(px, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(px, x, y, c)

def art(px, rows, x0, y0, pal, flip=False):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch != "." and ch in pal:
                xx = x0 + (len(r) - 1 - i if flip else i)
                put(px, xx, y0 + j, pal[ch])

def lerp_dither(px, x, y, a, b, t):
    """t 0..1 를 4x4 베이어로 두 색 사이 점 섞기"""
    put(px, x, y, b if t * 16 > BAYER[y % 4][x % 4] + 0.5 else a)

# ---------------- 글자 ----------------
def glyph_mask(txt, font, scale):
    f = ImageFont.truetype(font, 11)
    l, t, r, b = f.getbbox(txt)
    m = Image.new("L", (r - l + 2, b - t + 2), 0)
    dd = ImageDraw.Draw(m); dd.fontmode = "1"
    dd.text((-l + 1, -t + 1), txt, font=f, fill=255)
    m = m.point(lambda v: 255 if v > 128 else 0)
    return m.resize((m.width * scale, m.height * scale), Image.NEAREST)

def build_title():
    """굵기 2점으로 고정한 손글자. 사선은 1:2 계단만 쓴다."""
    pts = set()
    def hbar(x0, x1, y, ox):
        for x in range(x0, x1 + 1):
            pts.add((ox + x, y)); pts.add((ox + x, y + 1))
    def vbar(x, y0, y1, ox):
        for y in range(y0, y1 + 1):
            pts.add((ox + x, y)); pts.add((ox + x + 1, y))
    def diag(xs, y0, y1, d, ox):
        for y in range(y0, y1 + 1):
            x = xs + d * ((y - y0) // 2)
            pts.add((ox + x, y)); pts.add((ox + x + 1, y))
    # 서
    o = 0
    diag(8, 1, 18, -1, o); diag(4, 9, 18, 1, o); hbar(10, 13, 9, o); vbar(14, 0, 19, o)
    # 가
    o = 21
    hbar(0, 9, 2, o); vbar(8, 2, 9, o); diag(8, 10, 19, -1, o); vbar(13, 0, 19, o); hbar(15, 17, 9, o)
    # 은
    o = 42
    hbar(5, 12, 0, o); hbar(5, 12, 6, o); vbar(3, 2, 5, o); vbar(13, 2, 5, o)
    for p in ((4, 1), (13, 1), (4, 6), (13, 6)):
        pts.add((o + p[0], p[1]))
    hbar(0, 17, 10, o); vbar(2, 13, 19, o); hbar(2, 15, 18, o)
    w = max(x for x, _ in pts) + 1; h = max(y for _, y in pts) + 1
    m = Image.new("L", (w, h), 0)
    for p in pts:
        m.putpixel(p, 255)
    return m

def build_title_en():
    import names_en
    pts = names_en.word("SEO GAEUN")
    w = max(x for x, _ in pts) + 1; h = max(y for _, y in pts) + 1
    m = Image.new("L", (w, h), 0)
    for p in pts:
        m.putpixel(p, 255)
    return m

TITLE = None
LETTER_X = [0, 14, 28, 48, 62, 76, 90, 104]   # 글자마다 시작 x (SEO, 띄어쓰기, GAEUN)
TITLE_X, TITLE_Y = 20, 16
SUB1 = glyph_mask("게임 UI 아티스트", FONT, 1)
SUB2 = glyph_mask("테크니컬 아트", FONT, 1)

def draw_title(px, x0, y0, wave, press=0):
    global TITLE
    if TITLE is None:
        TITLE = build_title_en()
    tp = TITLE.load(); w, h = TITLE.size
    on = {(x, y) for x in range(w) for y in range(h) if tp[x, y]}
    # 글자마다 위아래로 한 칸씩 출렁(완급: 사인)
    def dy(x):
        col = sum(1 for lx in LETTER_X if x >= lx) - 1
        if col == 7 and press:
            return press
        return -1 if math.sin(wave - col * 0.9) > 0.55 else 0
    sh = [(x + 2, y + 2) for (x, y) in on]
    for (x, y) in sh:
        put(px, x0 + x, y0 + y + dy(x - 2), C["pinkD"])
    outline = set()
    for (x, y) in on:
        for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + ax, y + ay) not in on:
                outline.add((x + ax, y + ay))
    for (x, y) in outline:
        put(px, x0 + x, y0 + y + dy(x), C["k"])
    for (x, y) in on:
        put(px, x0 + x, y0 + y + dy(x), C["txt"])

def draw_mask(px, m, x0, y0, c):
    p = m.load()
    for y in range(m.height):
        for x in range(m.width):
            if p[x, y]:
                put(px, x0 + x, y0 + y, c)

# ---------------- 인물 (등 쪽 3/4, 오른쪽 화면을 본다) ----------------
HEAD = [
    "..kkk...kkkkkk......",
    ".khhhk.khhhhhhkk....",
    "khLhhkkhLLhhhhhhk...",
    "khhhhkcchLhhhhhhhk..",
    ".kkhhkcchhLhhhhhhrk.",
    "...kkkkhhhhhhhhhhrk.",
    "....khhhhhhhhhhhssk.",
    "....khhLhhhhhhhsssk.",
    "....khhhLhhhhhhsbsk.",
    "....khhhhhhhhhhssk..",
    ".....khhhhhhhhhhkk..",
    ".....khhhhhhhhhk....",
    "......kkhhhhhhkk....",
]
TORSO = [
    "...kkcccckkk......",
    "..kccccccccck.....",
    ".kcccccccccccck...",
    ".kCccccccccccccck.",
    ".kCcccccccccccccck",
    ".kCCcccccccccccck.",
    ".kCCccccccccccck..",
    "..kCCcccccccccck..",
    "..kppppppppppppppk",
    "..kPpppppppppppppk",
    "...kkkkkkkkkkkkkk.",
]
ARM = ["kkk..", "ccck.", "ccCsk", "kkksk", "...k."]   # 화면 쪽으로 뻗은 팔과 손
PAL_P = {"k": C["k"], "h": C["hair"], "L": C["hairL"], "r": C["rim"], "s": C["skin"], "S": C["skinD"],
         "b": C["pinkL"], "c": C["pink"], "C": C["pinkD"], "p": C["pant"], "P": C["pantD"]}

CAT = [  # 둥글게 잠든 고양이
    "...k.k........",
    "..kwkwk.......",
    ".kwwwwwkkk....",
    "kwwwwwwwwwkk..",
    "kwwDwwwwwwwwk.",
    "kwwwwwwwwwwwk.",
    ".kDwwwwwwwwDk.",
    "..kkkkkkkkkk..",
]
PAL_CAT = {"k": C["k"], "w": C["cat"], "D": C["catD"]}

HEART = [(1, 0), (2, 0), (4, 0), (5, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
         (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
         (2, 4), (3, 4), (4, 4), (3, 5)]

# ---------------- 그려진 친구(말랑이) ----------------
def slime_mask(w, h):
    pts = set()
    for y in range(h):
        for x in range(w):
            nx = (x + 0.5 - w / 2) / (w / 2); ny = (y + 0.5 - h) / h   # 바닥이 평평한 반타원
            if nx * nx + ny * ny <= 1.0:
                pts.add((x, y))
    return pts

def slime_pixels(cx, yb, w, h, blink=False, look=0):
    m = slime_mask(w, h); x0 = cx - w // 2; y0 = yb - h + 1
    out = {}
    for (x, y) in m:
        edge = any((x + a, y + b) not in m for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        c = C["k"] if edge else C["pink"]
        if not edge and (y >= h - 3 or x >= w - 3 and y > h // 2):
            c = C["pinkD"]
        out[(x0 + x, y0 + y)] = c
    # 하이라이트
    hx_, hy_ = x0 + w // 2 - 3, y0 + 2
    for p in ((hx_, hy_), (hx_ + 1, hy_), (hx_, hy_ + 1)):
        if p in out and out[p] != C["k"]:
            out[p] = C["txt"]
    ey = y0 + max(2, h // 2 - 1); ex = cx + look
    for xx in (ex - 2, ex + 2):
        if blink:
            out[(xx, ey + 1)] = C["k"]
        else:
            out[(xx, ey)] = C["k"]; out[(xx, ey + 1)] = C["k"]
    out[(ex - 3, ey + 2)] = C["pinkL"]; out[(ex + 3, ey + 2)] = C["pinkL"]
    return out

SLIME_PIX = slime_pixels(255, 47, 13, 10)
DOTS_ON_SCREEN = sorted(SLIME_PIX, key=lambda p: (p[1], p[0]))

HOPS = [  # (출발 x, 바닥 y, 도착 x, 바닥 y, 높이, 프레임)
    (255, 47, 252, 27, 9, 7),     # 화면 밖으로 튀어나와 모니터 위로
    (252, 27, 196, 44, 10, 9),    # 창턱으로
    (196, 44, 130, 15, 12, 12),   # 이름 끝 글자 위로
]
N = 96
DRAW_END = 30

def slime_state(f):
    if f < DRAW_END:
        return {"phase": "draw", "n": int(len(DOTS_ON_SCREEN) * f / (DRAW_END - 4))}
    t = f - DRAW_END
    if t < 8:   # 깨어나서 두리번, 마지막 두 칸은 웅크림(예비 동작)
        st = {"phase": "idle", "x": 255, "yb": 47, "w": 13, "h": 10, "blink": t in (1,), "look": (0, 0, -1, -1, 1, 1, 0, 0)[t]}
        if t >= 6:
            st.update(w=15, h=8)
        return st
    t -= 8
    for (x0, y0, x1, y1, ap, n) in HOPS:
        if t < n:
            u = (t + 1) / n
            x = round(x0 + (x1 - x0) * u)
            yb = round(y0 + (y1 - y0) * u - ap * 4 * u * (1 - u))
            w, h = (11, 12) if u < 0.5 else (12, 11)   # 올라갈 땐 늘어나고
            return {"phase": "hop", "x": x, "yb": yb, "w": w, "h": h, "look": -1}
        t -= n
        if t < 3:   # 착지: 납작 → 통통 → 제자리
            w, h = [(17, 7), (12, 11), (13, 10)][t]
            st = {"phase": "sit" if (x1, y1) == (130, 15) else "idle", "x": x1, "yb": y1, "w": w, "h": h, "look": -1}
            if (x1, y1) == (130, 15):
                st["press"] = [1, 1, 0][t]
            return st
        t -= 3
    # 이름 위에 앉아서 쉼
    if f < N - 4:
        return {"phase": "sit", "x": 130, "yb": 15, "w": 13, "h": 10, "blink": (f % 20) in (5, 6), "look": 1 if (f // 10) % 2 else -1}
    return {"phase": "pop", "k": f - (N - 4)}

def draw_slime(px, st, clip):
    pix = slime_pixels(st["x"], st["yb"], st["w"], st["h"], st.get("blink", False), st.get("look", 0))
    for (x, y), c in pix.items():
        if clip and not (clip[0] <= x <= clip[2] and clip[1] <= y <= clip[3]):
            continue
        put(px, x, y, c)

random.seed(7)
STARS = [(random.randint(178, 226), random.randint(13, 40)) for _ in range(14)]

def frame(f):
    im = Image.new("RGBA", (NW, NH)); px = im.load()
    t = f / N
    # 벽: 세 단 디더
    for y in range(NH):
        for x in range(NW):
            if y < 22:
                put(px, x, y, C["w0"])
            elif y < 30:
                lerp_dither(px, x, y, C["w0"], C["w1"], (y - 22) / 8)
            elif y < 48:
                put(px, x, y, C["w1"])
            elif y < 56:
                lerp_dither(px, x, y, C["w1"], C["w2"], (y - 48) / 8)
            else:
                put(px, x, y, C["w2"])
    rect(px, 0, 70, NW - 1, NH - 1, C["fl"])
    for x in range(0, NW, 2):
        put(px, x, 70, C["fl2"])

    # 창문
    wx0, wy0, wx1, wy1 = 172, 8, 232, 46
    rect(px, wx0, wy0, wx1, wy1, C["frame"])
    for y in range(wy0 + 2, wy1 - 1):
        for x in range(wx0 + 2, wx1 - 1):
            lerp_dither(px, x, y, C["sky"], C["sky2"], (y - wy0) / (wy1 - wy0))
    rect(px, (wx0 + wx1) // 2, wy0, (wx0 + wx1) // 2 + 1, wy1, C["frame"])
    rect(px, wx0, wy1 - 1, wx1 + 2, wy1 + 1, C["frameL"])
    for i, (sx, sy) in enumerate(STARS):
        if abs(sx - (wx0 + wx1) // 2) < 2:
            continue
        ph = (f + i * 7) % 24
        if ph < 3:
            put(px, sx, sy, C["star"]); put(px, sx - 1, sy, C["star2"]); put(px, sx + 1, sy, C["star2"])
            put(px, sx, sy - 1, C["star2"]); put(px, sx, sy + 1, C["star2"])
        elif ph < 14:
            put(px, sx, sy, C["star2"])
    # 초승달
    for y in range(-5, 6):
        for x in range(-5, 6):
            if x * x + y * y <= 25 and (x - 2) ** 2 + (y + 1) ** 2 > 16:
                put(px, 220 + x, 18 + y, C["moon"])

    # 램프 빛 웅덩이 (책상 위, 디더로 번짐)
    for y in range(36, 70):
        for x in range(250, 318):
            d = math.hypot((x - 296) / 1.4, y - 54)
            a = max(0, 1 - d / 26)
            if a > 0 and px[x, y] in (C["w1"], C["w2"], C["w0"]):
                lerp_dither(px, x, y, px[x, y], C["w2"] if a < .5 else hx("3a3566"), a)

    # 책상
    rect(px, 198, 52, 316, 53, C["woodL"]); rect(px, 198, 54, 316, 56, C["wood"]); rect(px, 198, 57, 316, 57, C["woodD"])
    rect(px, 202, 58, 204, 69, C["woodD"]); rect(px, 310, 58, 312, 69, C["woodD"])
    # 모니터 (펜 디스플레이)
    mx0, my0, mx1, my1 = 238, 28, 272, 50
    rect(px, mx0, my0, mx1, my1, C["bez"]); rect(px, mx0, my0, mx1, my0, C["bezL"])
    rect(px, mx0 + 2, my0 + 2, mx1 - 2, my1 - 2, C["scr"])
    for y in range(my0 + 2, my1 - 1):
        for x in range(mx0 + 2, mx1 - 1):
            if (x + y) % 4 == 0 and y > my0 + 12:
                put(px, x, y, hx("9aeaff"))
    rect(px, 253, 51, 257, 51, C["bezL"]); rect(px, 250, 51, 260, 51, C["bez"])
    # 화면 속 친구: 한 점씩 그려지고, 살아나서 화면 밖으로 뛰쳐나간다
    sl = slime_state(f)
    if sl["phase"] == "draw":
        for (x, y) in DOTS_ON_SCREEN[:sl["n"]]:
            put(px, x, y, SLIME_PIX[(x, y)])
        if sl["n"] < len(DOTS_ON_SCREEN):
            cx, cy = DOTS_ON_SCREEN[sl["n"]]
            rect(px, cx - 1, cy - 1, cx + 1, cy + 1, C["k"]); put(px, cx, cy, C["txt"])
        cur = DOTS_ON_SCREEN[min(sl["n"], len(DOTS_ON_SCREEN) - 1)]
    else:
        cur = (255, 40)
    # 화면 안에 있는 동안은 화면으로 잘라 그린다
    if sl["phase"] in ("idle", "hop") and sl.get("in_screen"):
        clip = (mx0 + 2, my0 + 2, mx1 - 2, my1 - 2)
    else:
        clip = None
    if sl["phase"] in ("idle", "hop", "sit"):
        draw_slime(px, sl, clip if sl["phase"] == "idle" else None)
    # 모니터 빛이 책상에 번진다
    for x in range(240, 271):
        put(px, x, 52, hx("c9f4ff"))

    # 머그와 김
    rect(px, 278, 46, 284, 51, C["mug"]); rect(px, 278, 46, 278, 51, C["mugD"]); rect(px, 285, 47, 286, 49, C["mugD"])
    rect(px, 278, 45, 284, 45, C["k"])
    for i, base in enumerate((279, 282)):
        for s in range(5):
            yy = 43 - s - ((f // 2 + i * 3) % 6)
            xx = base + (1 if (s + f // 3 + i) % 4 < 2 else 0)
            if yy > 30 and (s + f // 2) % 3:
                put(px, xx, yy, C["steam"])

    # 램프
    rect(px, 300, 50, 306, 51, C["k"]); rect(px, 302, 34, 303, 49, C["k"])
    for i in range(6):
        put(px, 303 - i, 33 - i // 2, C["k"])
    for y in range(32, 52):
        half = (y - 31) * 0.55
        for x in range(int(296 - half), int(296 + half) + 1):
            if (x + y) % 2 == 0 and (y - 32) < 19:
                if px[x, y] in (C["w1"], C["w2"], C["w0"]):
                    put(px, x, y, hx("4a3f6a") if y > 40 else hx("5a4a6e"))
    for x in range(284, 310):
        put(px, x, 52, C["glow"]) if x % 3 else None
    rect(px, 292, 27, 300, 30, C["lamp"]); rect(px, 292, 30, 300, 30, C["lampD"]); rect(px, 293, 31, 299, 31, C["glow"])

    # 고양이 (모니터 옆) : 숨 쉴 때 등이 한 칸 오르내림, 꼬리 흔들림
    breathe = 1 if math.sin(t * 2 * math.pi * 2) > 0.3 else 0
    cat = CAT if not breathe else [CAT[0], CAT[1], CAT[2]] + CAT[2:7] + [CAT[7]]
    art(px, CAT, 284, 44 + (0 if breathe else 0), PAL_CAT)
    if breathe:
        rect(px, 288, 46, 292, 46, C["cat"])
    tail = (f // 6) % 4
    tx = [(298, 50), (299, 49), (299, 48), (299, 49)][tail]
    put(px, tx[0], tx[1], C["cat"]); put(px, tx[0] - 1, tx[1] + 1, C["cat"]); put(px, tx[0] + 1, tx[1] - 1, C["k"])
    # zz
    zf = (f % 24)
    if zf < 18:
        zx, zy = 286 + zf // 6, 40 - zf // 3
        put(px, zx, zy, C["sub"]); put(px, zx + 1, zy, C["sub"]); put(px, zx + 1, zy + 1, C["sub"]); put(px, zx, zy + 2, C["sub"]); put(px, zx + 1, zy + 2, C["sub"])

    # 의자
    rect(px, 206, 38, 209, 62, C["chair"]); rect(px, 206, 38, 206, 62, C["chairL"])
    rect(px, 206, 60, 234, 62, C["chair"]); rect(px, 206, 60, 234, 60, C["chairL"])
    rect(px, 219, 63, 221, 68, C["k"]); rect(px, 213, 69, 227, 69, C["k"])

    # 인물: 그리는 박자에 맞춰 손이 움직이고 몸이 살짝 숙여진다
    stroke = sl["phase"] == "draw"
    lean = 1 if stroke and (f // 2) % 4 in (1, 2) else 0
    blink = f in (40, 41)
    head = [r for r in HEAD]
    art(px, TORSO, 210, 49, PAL_P)
    art(px, head, 209 + lean, 36, PAL_P)
    # 팔: 손끝이 화면의 커서를 따라간다
    hxp = 230 + ((cur[0] - 248) // 3 if stroke else 0)
    hyp = 50 - (1 if stroke and f % 2 else 0)
    art(px, ARM, hxp - 4, hyp, PAL_P)
    # 펜
    put(px, hxp + 1, hyp - 1, C["lamp"]); put(px, hxp + 2, hyp - 2, C["lamp"]); put(px, hxp + 3, hyp - 3, C["k"])
    if blink:
        pass  # 등 쪽이라 눈은 안 보인다

    # 글자 (친구가 내려앉으면 '은'이 한 칸 눌린다)
    draw_title(px, TITLE_X, TITLE_Y, t * 2 * math.pi, press=sl.get("press", 0))
    if sl["phase"] == "sit":
        draw_slime(px, sl, None)
    if sl["phase"] == "pop":
        k = sl["k"]
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            put(px, 130 + dx * (2 + k * 2), 10 + dy * (2 + k * 2), C["txt"] if k < 2 else C["pinkL"])
    draw_mask(px, SUB1, 19, 45, C["sub"])
    draw_mask(px, SUB2, 19, 58, C["sub"])
    return im.resize((NW * SC, NH * SC), Image.NEAREST)

if __name__ == "__main__":
  frames = [frame(f) for f in range(N)]
  durs = [80] * N
  frames[0].save(os.path.join(HERE, "..", "assets", "banner-room.png"), save_all=True, append_images=frames[1:], duration=durs, loop=0)
  g = [fr.convert("RGB").quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for fr in frames]
  g[0].save(os.path.join(HERE, "room_banner_preview.gif"), save_all=True, append_images=g[1:], duration=durs, loop=0)
  frames[70].convert("RGB").save(os.path.join(HERE, "room_still.png"))
  print("ok")
