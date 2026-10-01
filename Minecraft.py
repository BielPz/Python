from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Criação do jogo estilo Minecraft com Ursina Engine
app = Ursina()
# Criação do céu
Sky()

# Criação do chão
for x in range(20):
    for z in range(20):
        Entity(model='cube', 
               color=color.lime,
               texture='white_cube',
               collider='box',
               position=(x, 0, z))

# Criação do jogador
jogador = FirstPersonController(position=(8, 1, 2))

cores = {'1': color.red, 
         '2': color.green, 
         '3': color.blue, 
         '4': color.yellow, 
         '5': color.orange, 
         '6': color.pink, 
         '7': color.rgb(0.5, 0, 0.5),
         '8': color.cyan, 
         '9': color.white
         }

cor = color.red

def input(key):
    global cor                      # Permite alterar a cor globalmente
    if key in cores:
        cor = cores[key]
    alvo = mouse.hovered_entity     # Pega o bloco que o mouse está apontando
    if not alvo:
        return
    # Cria um bloco com o botão direito do mouse
    if key == 'right mouse down':
        Entity(model='cube',
            color=cor,
            texture='white_cube',
            collider='box',
            position=alvo.position + mouse.normal)
    # Destroi o bloco clicado com o botão esquerdo do mouse
    if key == 'left mouse down':
        destroy(alvo)
    # Pula para cima
    if key == 'space':
        jogador.position = (jogador.position[0], jogador.position[1] + 1, jogador.position[2])
    # Abaixa para baixo
    if key == 'left control':
        jogador.position = (jogador.position[0], jogador.position[1] - 1, jogador.position[2])
    # Aumenta a velocidade do jogador
    if held_keys['shift']:
        jogador.speed = 10  
    else:
        jogador.speed = 5
    # Sai do jogo
    if key == 'escape':
        application.quit()  

app.run()