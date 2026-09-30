import pygame
import math

pygame.init()
tela = pygame.display.set_mode((600,400))
relogio = pygame.time.Clock()
mapa = [
    "###############",
    "#.....#.......#",
    "#.....#.......#",
    "#..#.....##...#",
    "#.............#",
    "#.....##..#...#",
    "####..#...#...#",
    "#.........#...#",
    "#......#......#",
    "###############"
]
T = 8
x, y, ang = 1.5, 4.5, 0.0
FOV = math.pi / 3
COLUNAS = 120
L = 600 / COLUNAS
inimigos = [[9.5, 4.5], [11.5, 1.5], [8.5, 7.5]]
tiro = 0

def parede(px, py):
    return mapa[int(py)][int(px)] == "#"

def raio(a):
    c, s = math.cos(a), math.sin(a)
    d = 0
    while not parede(x + c * d, y + s * d):
        d += 0.02
    return d

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                tiro = 6

    k = pygame.key.get_pressed()
    ang += (k[pygame.K_RIGHT] - k[pygame.K_LEFT]) * 0.05
    passo = (k[pygame.K_UP] - k[pygame.K_DOWN]) * 0.08
    dx = math.cos(ang) * passo
    dy = math.sin(ang) * passo
    if not parede(x + dx * 4, y):
        x += dx
    if not parede(x, y + dy * 4):
        y += dy

    tela.fill("gray10")
    pygame.draw.rect(tela, "sienna4", (0, 200, 600, 200))
    dist = []
    for i in range(COLUNAS):
        a = ang - FOV / 2 + FOV * i / COLUNAS
        d = raio(a)
        px = x + math.cos(a) * d
        py = y + math.sin(a) * d
        d *= math.cos(a - ang)
        dist.append(d)
        luz = max(30, 230 - d * 22)
        if abs(px - round(px)) < 0.03:
            luz *= 0.7
        h = min(400, 400 / d)
        cor = (luz, luz * 0.9, luz * 0.75)
        faixa = (i * L, 200 - h / 2, L, h)
        pygame.draw.rect(tela, cor, faixa)
        pygame.draw.line(tela, "yellow", (x * T, y * T),
                         (px * T, py * T))

    inimigos.sort(key=lambda e: -math.dist(e, (x, y)))
    for e in inimigos[:]:
        dx, dy = e[0] - x, e[1] - y
        de = math.hypot(dx, dy)
        if de > 0.8:
            e[0] -= dx / de * 0.03
            e[1] -= dy / de * 0.03
        rel = math.atan2(dy, dx) - ang
        rel = (rel + math.pi) % (2 * math.pi) - math.pi
        sx = 300 + rel / (FOV / 2) * 300
        col = int(sx / L)
        if not 0 <= col < COLUNAS or dist[col] < de:
            continue
        h = 400 / de
        corpo = pygame.Rect(0, 0, h * 0.5, h *0.7)
        corpo.midbottom = (sx, 200 + h / 2)
        pygame.draw.ellipse(tela, "darkred", corpo)
        for ox in (sx - h * 0.1, sx + h * 0.1):
            olho = (ox, corpo.y + h * 0.2)
            pygame.draw.circle(tela, "gold", olho, h / 20)
        if tiro == 6 and abs(sx - 300) < h * 0.25:
            inimigos.remove(e)
            tiro = 5

    for ny, linha in enumerate(mapa):
        for nx, c in enumerate(linha):
            if c == "#":
                bloco = (nx * T, ny * T, T, T)
                pygame.draw.rect(tela, "gray40", bloco)
    for ex, ey in inimigos:
        pos = (ex * T, ey * T)
        pygame.draw.circle(tela, "red", pos, 3)
    pygame.draw.circle(tela, "white", (x * T, y *T), 5)

    if tiro > 0:
        pygame.draw.circle(tela, "orange", (300, 270), 34)
        pygame.draw.circle(tela, "yellow", (300, 270), 18)
        tiro -= 1
    arma = [(255, 400), (280, 320), (320, 320), 
            (345, 400)]
    pygame.draw.polygon(tela, "gray35", arma)
    pygame.draw.rect(tela, "gray20", (288, 280, 25, 60))
    pygame.draw.circle(tela, "white", (300, 200), 3)
    pygame.display.flip()
    relogio.tick(30)

pygame.quit()