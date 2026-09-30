import pygame
import random

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((600,400))
relogio = pygame.time.Clock()

# Definição das peças do Tetris
# ([(x,y),(x,y),(x,y),(x,y)], "cor")
PECAS = [
    ([(0,1),(1,1),(2,1),(3,1)], "cyan"),
    ([(1,0),(2,0),(1,1),(2,1)], "blue"),
    ([(1,0),(0,1),(1,1),(2,1)], "orange"),
    ([(0,0),(0,1),(1,1),(2,1)], "yellow"),
    ([(2,0),(0,1),(1,1),(2,1)], "limegreen"),
    ([(1,0),(2,0),(0,1),(1,1)], "red"),
    ([(0,0),(1,0),(1,1),(2,1)], "purple")
]

largura, altura = 18, 20  # Dimensões da grade do Tetris

# Definição da grade do Tetris
grade = [[None] * largura for _ in range(altura)]  # Grade inicial vazia

# Função para escolher uma nova peça
def nova_peca():
    blocos, cor = random.choice(PECAS)
    return blocos, cor, 3, 0  # posição inicial (x=3, y=0)

# Função para verificar se a posição da peça é válida
def livre(blocos, px, py):
    for x, y in blocos:
        gx, gy = x + px, y + py
        if not (0 <= gx < largura and 0 <= gy < altura) or grade[gy][gx] is not None:
            return False
    return True

# Função para gerar a peça na grade
def bloco(x, y, cor):
    r = (75 + x * 20, y * 20, 19, 19)
    pygame.draw.rect(tela, cor, r, 0, 3)

# Variáveis iniciais do jogo
blocos, cor, px, py = nova_peca()               # peça atual
lados = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1}  # Controle de movimento lateral
queda = 0
pontos = 0
rodando = True


# Loop principal do jogo
while rodando:
    agora = pygame.time.get_ticks()                     # Tempo atual em milissegundos
    for evento in pygame.event.get():
        potencializar = pygame.key.get_pressed()        # Aumentar efeito do controle de movimento
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            k = evento.key
            dx = lados.get(k, 0)
            if dx and livre(blocos, px + dx, py):
                if potencializar[pygame.K_LSHIFT] and livre(blocos, px + dx * 2, py):  # Movimento rápido com Shift
                    px += dx * 2
                else:
                    px += dx
            if k == pygame.K_UP and cor != "blue":  # Não rotaciona o bloco azul
                girada = [(2 - y, x) for x, y in blocos]  # Rotação 90 graus
                if livre(girada, px, py):
                    blocos = girada
            if k == pygame.K_SPACE:
                while livre(blocos, px, py + 1):
                    py += 1
                queda = 0
            if k == pygame.K_DOWN:
                if potencializar[pygame.K_LSHIFT]:
                    if livre(blocos, px, py + 1) and livre(blocos, px, py + 2):
                        py += 2
                        queda = agora
                else:
                    if livre(blocos, px, py + 1):
                        py += 1
                        queda = agora

    # Atualiza a posição da peça com base no tempo
    if agora - queda > 500:
        queda = agora
        if livre(blocos, px, py + 1):
            py += 1
        else:
            # Adiciona a peça à grade e verifica linhas completas
            for x, y in blocos:
                grade[y + py][x + px] = cor
            grade = [L for L in grade if None in L] # Remove linhas completas
            cheias = altura - len(grade)
            pontos += cheias * 100
            vazias = [[None] * largura for _ in range(cheias)]
            grade = vazias + grade
            blocos, cor, px, py = nova_peca()
            if not livre(blocos, px, py):
                grade = [[None] * largura for _ in range(altura)]  # Reinicia a grade
                pontos = 0

    # Desenha a tela do jogo
    tela.fill((20, 20, 35))

    # Desenha a grade e as peças
    for y in range(altura):
        for x in range(largura):
            bloco(x, y, grade[y][x] or (40, 40, 60))
    for x, y in blocos:
        bloco(x + px, y + py, cor)
    
    # Desenha o placar
    placar = f"PONTOS: {pontos}".rjust(10)
    texto = pygame.font.SysFont("Arial", 24).render(placar, True, "white")
    tela.blit(texto, (450, 40))

    # Atualiza a tela e controla o tempo do jogo
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()