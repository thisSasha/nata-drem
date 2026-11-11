from PIL import Image
im = Image.open('original.png').convert('RGB')
W, H = im.size
px = im.load()

def cls(r, g, b):
    lum = 0.299*r + 0.587*g + 0.114*b
    if lum < 90: return 'H'                                   # волосы / тёмное
    if lum > 205 and max(r,g,b)-min(r,g,b) < 25: return 'T'   # майка (белое)
    if max(r,g,b)-min(r,g,b) > 35 and r > g > b: return 'S'   # кожа (загар)
    return 'B'                                                # фон

def runs_at(y):
    row = [cls(*px[x, y][:3]) for x in range(W)]
    runs = []; cur = row[0]; start = 0
    for x in range(1, W):
        if row[x] != cur:
            runs.append((cur, start, x-1)); cur = row[x]; start = x
    runs.append((cur, start, W-1))
    return [r for r in runs if r[2]-r[1] >= 2]

out = []
out.append(f"original.png {W}x{H}")
out.append("")
out.append("== Вертикальные разрезы (классы: H=волосы, T=майка, S=кожа, B=фон) ==")
for y in range(60, H, 25):
    rs = runs_at(y)
    out.append(f"y={y}: " + ' '.join(f"{c}{a}-{b}" for c, a, b in rs))

out.append("")
out.append("== Зазор волосы/рука справа (x 286-305) ==")
for y in [330, 360, 390, 420, 450, 480, 505]:
    out.append(f"y={y}: " + ' '.join(f"{x}:{px[x, y]}" for x in range(286, 306, 2)))

out.append("")
out.append("== Слева, край волос/рука (x 60-100) ==")
for y in [420, 450, 470, 490, 505]:
    out.append(f"y={y}: " + ' '.join(f"{x}:{px[x, y]}" for x in range(60, 100, 3)))

out.append("")
out.append("== Край волос по строкам (без виньетки по краям) ==")
for y in range(70, H-8, 20):
    xs = [x for x in range(8, W-8) if cls(*px[x, y][:3]) == 'H']
    if xs:
        out.append(f"y={y}: волосы x {min(xs)}-{max(xs)}")

text = '\n'.join(out)
with open('analysis.txt', 'w') as f:
    f.write(text)
print(text)
