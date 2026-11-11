from PIL import Image, ImageFilter
from collections import deque

im = Image.open('original.png').convert('RGB')
W, H = im.size
px = im.load()

# приоритет: 1) фон #9F9689  2) тело: майка #A09E9E + кожа #936144  3) волосы #161412 (остаток тёмного)
def cls(r, g, b):
    lum = 0.299*r + 0.587*g + 0.114*b
    warm = r - b          # фон и кожа тёплые, майка нейтрально-холодная
    if lum < 95: return 0                        # тёмное -> кандидат в волосы
    if lum > 215: return 1                       # яркое белое -> майка
    if warm >= 45: return 1                      # насыщенный загар -> кожа(тело)
    if 8 <= warm <= 44: return 3                 # тёплый серо-бежевый -> фон
    if warm >= -2: return 1                      # нейтральное светлое -> майка (тень рукава)
    return 3                                     # слегка тёплое светлое -> фон

mask = Image.new('L', (W, H))
mask.putdata([cls(*px[x, y][:3]) for y in range(H) for x in range(W)])
mask = mask.filter(ImageFilter.ModeFilter(7))
m = mask.load()
for x in range(W):
    for y in list(range(3)) + list(range(H-4, H)): m[x, y] = 3   # виньетка краёв -> фон
for y in range(H):
    for x in list(range(3)) + list(range(W-3, W)): m[x, y] = 3

# связные компоненты, 4-соседство
label = [[-1]*W for _ in range(H)]
comps = []
for y in range(H):
    for x in range(W):
        if label[y][x] == -1:
            c = m[x, y]; comp = []
            q = deque([(x, y)]); label[y][x] = len(comps)
            while q:
                cx, cy = q.popleft(); comp.append((cx, cy))
                for nx, ny in ((cx-1,cy),(cx+1,cy),(cx,cy-1),(cx,cy+1)):
                    if 0 <= nx < W and 0 <= ny < H and label[ny][nx] == -1 and m[nx, ny] == c:
                        label[ny][nx] = len(comps); q.append((nx, ny))
            comps.append((c, comp))

# мелкие блоки (<400 px) перекрашиваем в класс крупного соседа, если нет - остаток
info = []
final = {}
for i, (c, comp) in enumerate(comps):
    xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
    info.append([i, c, len(comp), min(xs), max(xs), min(ys), max(ys)])
    final[i] = c
big_ids = [i for i in info if i[2] >= 400]
for i, c, n, x0, x1, y0, y1 in info:
    if n < 400:
        # сосед по классу
        neigh = set()
        for x, y in comps[i][1]:
            for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0 <= nx < W and 0 <= ny < H:
                    j = label[ny][nx]
                    if j != i and comps[j][0] != c and comps[j][1] and len(comps[j][1]) >= 400:
                        neigh.append if False else neigh.add(comps[j][0])
        final[i] = neigh.pop() if len(neigh) == 1 else 9

PAL = {0: (66, 76, 230), 1: (60, 190, 90), 3: (255, 210, 70), 9: (235, 85, 120)}
out = Image.new('RGB', (W, H)); op = out.load()
for i, (c, comp) in enumerate(comps):
    r, g, b = PAL[final[i]]
    for x, y in comp: op[x, y] = (r, g, b)
out.save('blocks.png')

names = {0: 'волосы', 1: 'тело', 3: 'фон', 9: 'ОСТАТОК'}
lines = [f"blocks.png {W}x{H}", "== Компоненты >=400px =="]
for i, c, n, x0, x1, y0, y1 in sorted(info, key=lambda t: -t[2]):
    if n >= 400:
        lines.append(f"{names[final[i]]:8s} id={i:3d} px={n:7d} x {x0}-{x1}  y {y0}-{y1}")
text = '\n'.join(lines)
with open('blocks.txt', 'w') as f: f.write(text)
print(text)
