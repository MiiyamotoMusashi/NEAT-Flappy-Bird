import pygame
from sys import exit
from pygame.locals import *
from pipe import *
from floor import Floor
import neat

gen = 0

# Imagens e sons que seram utilizados
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 512
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
IMAGES = {'bird': [
                    pygame.image.load('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\sprites\\default-bird.png').convert_alpha(),
                    pygame.image.load('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\sprites\\up-bird.png').convert_alpha(),
                    pygame.image.load('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\sprites\\falling-bird.png').convert_alpha()
                    ],
          'bg': pygame.transform.scale(pygame.image.load('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\sprites\\background.png').convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT)),
          }
SOUNDS = {
    'hit': pygame.mixer.Sound('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\soundefeccts\\hit.wav'),
    'point': pygame.mixer.Sound('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\soundefeccts\\point.wav'),
    'wing': pygame.mixer.Sound('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\soundefeccts\\wing.wav')
    }

for i, img in enumerate(IMAGES['bird']):
    IMAGES['bird'][i] = pygame.transform.scale(IMAGES['bird'][i], (IMAGES['bird'][i].get_width() + 5, IMAGES['bird'][i].get_height() + 5))

pygame.init()
pygame.font.init()

FONT_SCORE = pygame.font.SysFont('arial', 30)

# Classe que representa o pássaro
class Bird():
    # Constantes do pássaro
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    ROTATION_TIME = 5
    ANIMATION_TIME = 5
    FLAPPING = True
        
    def __init__(self, x, y) -> None:
        # Atributos
        self.x = int((SCREEN_WIDTH - IMAGES['bird'][0].get_width()) / 2)
        self.y = int((SCREEN_HEIGHT - IMAGES['bird'][0].get_width()) / 2)
        self.angle = 0
        self.height = self.y
        self.speed = 5
        self.time = 0
        self.count_images = 0
        self.flapped = False
        self.img = IMAGES['bird'][0]
        
    def move(self):
        if not self.flapped: # Se ele não estiver pulando ele é cai
            # Calculando a força da gravidade
            self.time += 0.5
            gravity = 2 * self.time / 3
            
            # Limitando a força da gravidade
            if gravity > 9:
                gravity = 9
                
            self.y += gravity

        else:
            self.flapped = False
            self.speed = 22
            self.height = self.y
            self.time = 0
            
            # Gira o passáro em 20°
            if self.y < self.height + 50:
                self.angle = 20
            
            # SOUNDS['wing'].play()
                
            self.y -= self.speed
    
    # Função que o deseha na tela
    def draw(self, screen):
        self.count_images += 1
        
        # Animação do bater de asas do pássaro
        if self.count_images < self.ANIMATION_TIME * 1:
            self.img = IMAGES['bird'][0]
        elif self.count_images < self.ANIMATION_TIME * 2:
            self.img = IMAGES['bird'][1]
        elif self.count_images < self.ANIMATION_TIME * 3:
            self.img = IMAGES['bird'][2]
        elif self.count_images < self.ANIMATION_TIME * 4:
            self.img = IMAGES['bird'][1]
        elif self.count_images < self.ANIMATION_TIME * 4 + 1:
            self.img = IMAGES['bird'][0]
            self.count_images = 0
            
        # Mostrando a imagem na tela
        imagem_rotacionada = pygame.transform.rotate(self.img, self.angle)
        pos_centro_imagem = self.img.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        screen.blit(imagem_rotacionada, retangulo.topleft)
        
    # Pegando a hitbox do passáro
    def mask(self):
        return pygame.mask.from_surface(self.img)


# Função que desenha a tela inteira
def DrawMain(screen, birds, pipes, floor, score) -> object:
    screen.blit(IMAGES['bg'], (0, 0))
    
    for bird in birds:
        bird.draw(screen)
        
    for pipe in pipes:
        pipe.draw(screen)
    
    floor.draw(screen)
    
    texto = FONT_SCORE.render(f"Pontuação: {score}", 1, (255, 255, 255))
    screen.blit(texto, (SCREEN_WIDTH - 10 - texto.get_width(), 10))
    
    txtgen = FONT_SCORE.render(f'Geração: {gen}', 1, (255, 255, 255))
    screen.blit(txtgen, (10, 10))
    
    pygame.display.update()

# Função do próprio jogo
def Main(genomes, config):
    global gen
    
    gen += 1
    
    birds = [] # Lista com cada passáro
    nets = [] # Redes neurais de cada respectivo passáro
    list_genome = [] # E o genoma
    
    # Criando os passáros, as redes e os genomas
    for _, genome in genomes:
        genome.fitness = 0 # Iniciando o fitness do genoma em 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        birds.append(Bird(184, 224))
        nets.append(net)
        list_genome.append(genome)

    floor = Floor(467) # Instanciando a classe Floor do chão
    pipes = [Pipe(600)] # Lista com os canos
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    
    running = True
    while running:
        clock.tick(32)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_m:
                    exit()
        
        # Orientando o passáro a qual cano ele tem que pegar a posição
        pipe_index = 0
        if len(pipes) > 1 and birds[0].x >= pipes[0].img_top.get_width() + pipes[0].x:
            pipe_index = 1
            
        for i, bird in enumerate(birds):
            bird.move()
            
            list_genome[i].fitness += 0.2 # "incentivando" o passáro a se mover
            
            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].y_bot))) # O resultado da rede neural
            
            if output[0] > 0.5: # Se o resultado for maior que 0.5 o passáro pula
                bird.flapped = True
                
        floor.move()
        
        add_pipe = False
        remove_pipes = [] # Lista de canos a serem removidos
        for pipe in pipes:
            for i, bird in enumerate(birds):
                # Verificando se o passaro atingiu o cano ou as extremidades da tela
                if bird.y >= SCREEN_HEIGHT - 70 or bird.y <= 0 or pipe.colision(bird):
                    SOUNDS['hit'].play()
                    
                    list_genome[i].fitness -= 2 # Subtraindo 2 do fitness do passáro para que ele entenda que nao é pra bater
                    
                    birds.pop(i)
                    nets.pop(i)
                    list_genome.pop(i)
                    
                    # Reiniciando o jogo e a velocidade dos canos
                    if len(birds) == 0:
                        running = False
                        pipe.SPEED = 5
                
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
                    score += 1
                    SOUNDS['point'].play()
                    
            pipe.move()
            
            if pipe.x + pipe.img_bot.get_width() < 0:
                remove_pipes.append(pipe)
                
        if add_pipe:
            pipes.append(Pipe(500))
            
            Pipe.SPEED += 0.1
            
            for genom in list_genome:
                genom.fitness += 5 # Incentivando o passáro a passar dos canos
            
        for pipe in remove_pipes:
            pipes.remove(pipe)
        
        DrawMain(screen, birds, pipes, floor, score)
        
def run(path_config):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, path_config) # Configuração da rede neural
    
    p = neat.Population(config) # Criando a população
    # Visualizando as informações de cada população
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    
    winner = p.run(Main, 50)
    
    print(f'\nBest genome\n{winner}')

if __name__ == '__main__':
    run('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\config.txt') # Caminho até o arquivo de configuraçao