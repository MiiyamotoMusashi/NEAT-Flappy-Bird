import pygame
from random import randint

pygame.init()
pygame.font.init()

class Pipe():
    # Constantes do cano
    IMG = [pygame.image.load('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\sprites\\pipe.png'), pygame.transform.rotate(pygame.image.load('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\sprites\\pipe.png'), 180)]
    IMG[0], IMG[1] = pygame.transform.scale(IMG[0], (IMG[0].get_width(), (IMG[0].get_height() + 100))), pygame.transform.scale(IMG[1], (IMG[1].get_width(), (IMG[1].get_height() + 50)))
    SPEED = 5
    
    def __init__(self, x) -> None:
        # Atributos dos canos
        self.x = x
        self.height = 0
        self.y_bot = 0
        self.y_bot = 0
        self.img_bot = self.IMG[0]
        self.img_top = self.IMG[1]
        self.passed = False
        self.set_height()
        
    def set_height(self):
        DISTANCE = randint(100, 150) # Distância entre os canos
        self.height = randint(0, 370)
        self.y_top = self.height - self.img_top.get_height() # Posição do cano de cima
        
        self.y_bot = self.height + DISTANCE # Posição do cano de baixo
    
    def move(self):
        # Limitando a velocidade
        if self.SPEED >= 8:
            self.SPEED = 8
            
        self.x -= self.SPEED # Movimentando os canos
        
    def draw(self, tela):
        # Desenhando cada cano
        tela.blit(self.img_bot, (self.x, self.y_bot))
        tela.blit(self.img_top, (self.x, self.y_top))
        
    def colision(self, bird):
        bird_mask = bird.mask()
        top_pipe_mask = pygame.mask.from_surface(self.img_top) # hitbox do cano de cima
        bot_pipe_mask = pygame.mask.from_surface(self.img_bot) # hitbox do cano de cima
        
        top_distance = (self.x - bird.x, self.y_top - round(bird.y))
        bot_distance = (self.x - bird.x, self.y_bot - round(bird.y))
        
        colision_top = bird_mask.overlap(top_pipe_mask, top_distance) # Retorna True se o passáro colidiu com o cano de cima
        colision_bot = bird_mask.overlap(bot_pipe_mask, bot_distance) # Retorna True se o passáro colidiu com o cano de baixo
        
        if colision_top or colision_bot: # Retorna True se o passáro colidiu com o cano
            return True
        else:
            return False