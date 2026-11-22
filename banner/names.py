"""이름 글자 시안 여러 벌. 모든 획 굵기는 시안 안에서 하나로 고정한다."""
import os
from PIL import Image
import room

HERE = os.path.dirname(os.path.abspath(__file__))


class G:
    def __init__(self):
        self.p = set()

    def box(self, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p.add((x, y))

    def diag(self, x, y0, y1, d, T, step):
        for y in range(y0, y1 + 1):
            xx = x + d * ((y - y0) // step)
            for k in range(T):
                self.p.add((xx + k, y))

    def ring(self, cx, cy, rx, ry, T):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                o = ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2
                i = ((x + .5 - cx) / (rx - T)) ** 2 + ((y + .5 - cy) / (ry - T)) ** 2
                if o <= 1 and i > 1:
                    self.p.add((x, y))

    def shift(self, ox):
        return {(x + ox, y) for x, y in self.p}


def soften(pts):
    """볼록한 모서리 한 점씩 깎아 둥글게"""
    out = set(pts)
    for (x, y) in pts:
        n = lambda a, b: (x + a, y + b) in pts
        if (not n(-1, 0) and not n(0, -1)) or (not n(1, 0) and not n(0, -1)) or \
           (not n(-1, 0) and not n(0, 1)) or (not n(1, 0) and not n(0, 1)):
            if sum(n(a, b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) == 2:
                out.discard((x, y))
    return out


def word(glyphs, gap):
    pts = set(); ox = 0
    for g, w in glyphs:
        pts |= g.shift(ox); ox += w + gap
    return pts


def seo(T, H=20, W=None):
    g = G(); W = W or 15 + T
    g.diag(6, 3, H - 1, -1, T, 3)                 # ㅅ 왼다리 (1:3)
    g.diag(4 + T - 1, 10, H - 1, 1, T, 2)         # ㅅ 오른다리 (1:2)
    vx = W - T
    g.box(vx - 4, 9, vx - 1, 9 + T - 1)           # ㅓ 짧은 가로
    g.box(vx, 0, W - 1, H)                        # ㅓ 세로
    return g, W

def ga(T, H=20):
    g = G()
    g.box(0, 3, 10, 3 + T - 1)                    # ㄱ 가로
    g.box(11 - T, 3, 10, 8)                       # ㄱ 꺾임
    g.diag(11 - T, 9, H - 1, -1, T, 2)            # ㄱ 삐침 (1:2)
    vx = 14
    g.box(vx, 0, vx + T - 1, H)                   # ㅏ 세로
    g.box(vx + T, 9, vx + T + 3, 9 + T - 1)       # ㅏ 짧은 가로
    return g, vx + T + 4

def eun(T, H=20, square=False):
    g = G(); W = 20
    if square:
        g.box(3, 0, 16, 7)
        inner = {(x, y) for x in range(3 + T, 17 - T) for y in range(T, 8 - T)}
        g.p -= inner
        for p in ((3, 0), (16, 0), (3, 7), (16, 7)):
            g.p.discard(p)
    else:
        g.ring(10, 4, 7, 4.2, T)
    g.box(0, 10, W - 1, 10 + T - 1)               # ㅡ
    g.box(2, 13 + (T > 2), 2 + T - 1, H)          # ㄴ 세로
    g.box(2, H - T + 1, 17, H)                    # ㄴ 가로
    return g, W

GAP = 5

def v_round():
    return soften(word([seo(3), ga(3), eun(3)], GAP))

def v_block():
    return word([seo(4), ga(4), eun(4, square=True)], GAP)

def v_tall():
    return word([seo(2, 24), ga(2, 24), eun(2, 24)], GAP)

def v_inline():
    return word([seo(4), ga(4), eun(4, square=True)], GAP)

def v_italic():
    pts = v_round(); H = max(y for _, y in pts)
    return {(x + (H - y) // 5, y) for x, y in pts}


def draw(px, pts, x0, y0, inline=False):
    C = room.C; put = room.put
    for (x, y) in pts:
        put(px, x0 + x + 2, y0 + y + 2, C["pinkD"])
    for (x, y) in pts:
        for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + a, y + b) not in pts:
                put(px, x0 + x + a, y0 + y + b, C["k"])
    for (x, y) in pts:
        put(px, x0 + x, y0 + y, C["txt"])
    if inline:
        for (x, y) in pts:
            if all((x + a, y + b) in pts for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))):
                put(px, x0 + x, y0 + y, C["pink"])
    if False:
        core = {p for p in pts if all((p[0] + a, p[1] + b) in pts for a in (-1, 0, 1) for b in (-1, 0, 1))}
        core = {p for p in core if all((p[0] + a, p[1] + b) in core or (p[0] + a, p[1] + b) not in pts for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
        for (x, y) in core:
            if (x + y) % 1 == 0 and ((x + 1, y) not in core or (x, y + 1) not in core):
                put(px, x0 + x, y0 + y, C["pinkL"])


if __name__ == "__main__":
    room.TITLE = Image.new("L", (1, 1), 0)
    variants = [("1 둥근 굵은 획", v_round(), False), ("2 네모 블록", v_block(), False),
                ("3 가는 세로", v_tall(), False), ("4 속선", v_inline(), True), ("5 둥근 기울임", v_italic(), False)]
    crops = []
    for name, pts, inl in variants:
        big = room.frame(5)
        im = big.resize((room.NW, room.NH), Image.NEAREST)
        px = im.load()
        h = max(y for _, y in pts) + 1
        draw(px, pts, 20, 23 - h // 2, inl)
        out = im.resize((room.NW * room.SC, room.NH * room.SC), Image.NEAREST)
        out.save(os.path.join(HERE, f"name_{name.split()[0]}.png"))
        crops.append(out.crop((0, 0, 700, 320)))
    sheet = Image.new("RGB", (700 * 2 + 20, 340 * 3), (255, 255, 255))
    for i, c in enumerate(crops):
        sheet.paste(c, ((i % 2) * 720, (i // 2) * 340))
    sheet.save(os.path.join(HERE, "name_options.png"))
    print("ok")
