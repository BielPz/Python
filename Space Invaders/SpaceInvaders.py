import pygame
import random

# Configurações iniciais
pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 30)
pygame.display.set_caption("Space Invaders - Python")

# Carrega e toca a música em loop
pygame.mixer.music.load("battle.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)  # Define o volume (0.0 a 1.0)

# Gera uma lista de estrelas com posições aleatórias
estrelas = [(random.randint(0, 599), random.randint(0, 399)) for _ in range(60)]

# Função para criar sprites a partir de uma representação em texto
def sprite(desenha, cor):
    img = pygame.Surface((len(desenha[0]) * 3, 
                          len(desenha) * 3),
                          pygame.SRCALPHA)
    for y, linha in enumerate(desenha):
        for x, c in enumerate(linha):
            if c == '#':
                img.fill(cor, (x * 3, y * 3, 3, 3)) # Preenche o pixel com a cor especificada
    return img

# Cria a nave do jogador usando a função sprite
nave = sprite(["......#......",
               ".....###.....",
               ".###########.",
               "#############",
               "#############"], (80, 230, 120))

x = 300         # Posição inicial da nave
tiro = None     # Ainda não há nenhum tiro ativo
cores = ["#ff5c8a", "#b87cff", "#5cd6ff", "#ffd75d"]

# imagens dos inimigos, cada uma com uma cor diferente
imagens = [sprite(["..#.....#..",
                   "...#...#...",
                   "..#######..",
                   ".##.###.##.",
                   "###########",
                   "#.#######.#",
                   "#.#.....#.#",
                   "...##.##..."], cor) for cor in cores]

def onda():
    return [
        (pygame.Rect(60 + c * 50, 40 + l * 34, 33, 24), imagens[l])
        for l in range(4)
        for c in range(8)
    ]

aliens = onda()
lado = 1

explosao = sprite(["#...#...#",
                   ".#..#..#.",
                   "..#...#..",
                   "##.....##",
                   "..#...#..",
                   ".#..#..#.",
                   "#...#...#"], "orange")

boom = None
boom_t = 0
pontos = 0
bombas = []
vidas = 3
choque = 0

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not tiro:
                tiro = pygame.Rect(x - 2, 350, 4, 14)

    # Atualiza a posição da nave com base nas teclas pressionadas
    teclas = pygame.key.get_pressed()
    x += (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * 5
    x = max(30, min(570, x))

    # Atualiza a posição do tiro, se houver
    if tiro:
        tiro.y -= 10
        if tiro.bottom < 0:
            tiro = None

    # Atualiza a posição dos inimigos e verifica colisões
    passo = lado * (1 + (32 - len(aliens)) // 8)
    if any(a.right + passo > 590 or a.left + passo < 10 for a, _ in aliens):
        lado = -lado
        for a, _ in aliens:
            a.y += 12
    else:
        for a, _ in aliens:
            a.x += passo

    # Verifica colisões entre o tiro e os inimigos
    for par in aliens:
        if tiro and tiro.colliderect(par[0]):
            aliens.remove(par)
            boom = par[0].move(3, 0)
            boom_t = 12
            tiro = None
            pontos += 10
            break
        if not aliens:
            aliens = onda()
        if any(a.bottom > 345 for a, _ in aliens):
            aliens = onda()
            pontos = 0

    # Gera bombas aleatoriamente a partir dos inimigos
    if random.random() < 0.03:
        a, _ = random.choice(aliens)
        bombas.append(pygame.Rect(a.centerx, a.bottom, 4, 12))

    # Atualiza a posição das bombas e verifica colisões com a nave
    for b in bombas[:]:
        b.y += 5
        if b.colliderect((x - 19, 355, 39, 15)):
            bombas.remove(b)
            vidas -= 1
            choque = 30
        elif b.top > 400:
            bombas.remove(b)
        if vidas == 0:
            aliens = onda()
            pontos = 0
            vidas = 3

    # Desenha o fundo da tela e as estrelas
    tela.fill((8, 8, 20))
    for estrela in estrelas:
        pygame.draw.circle(tela, (110, 110, 150), estrela, 1)

    # Desenha os inimigos na tela
    for a, img in aliens:
        tela.blit(img, a)

    # Desenha a explosão na tela, se houver
    if boom_t:
        tela.blit(explosao, boom)
        boom_t -= 1

    # Desenha o tiro na tela, se houver
    if tiro:
        pygame.draw.rect(tela, "white", tiro)

    # Desenha as bombas na tela
    for b in bombas:
        pygame.draw.rect(tela, (255, 90, 90), b)

    # Desenha a nave do jogador piscando quando colide com uma bomba
    if choque % 6 < 3:
        tela.blit(nave, (x - 19, 355))

    # Reduz o contador de choque a cada frame
    choque = max(0, choque - 1)

    placar = fonte.render(f"PONTOS: {pontos}", 1, "white")
    tela.blit(placar, (14, 10))
    texto_vidas = fonte.render(f"VIDAS: {vidas}", 1, "white")
    tela.blit(texto_vidas, (500, 10))

    # Atualiza a tela e define a taxa de quadros por segundo
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()