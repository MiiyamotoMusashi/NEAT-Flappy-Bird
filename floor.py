import pygame

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 512
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
IMG = pygame.image.load('C:\\Users\\Sorte Show\\Desktop\\Programação\\Projetos\\FlappyBird\\sprites\\base.png').convert_alpha()

class Floor():
    IMG = pygame.transform.scale(IMG, (SCREEN_WIDTH, IMG.get_height()))
    WIDTH_FLOOR = IMG.get_width()
    SPEED = 5
    
    def __init__(self, y) -> None:
        self.y = y
        self.x = 0
        self.x1 = self.WIDTH_FLOOR
        
    def move(self):
        # Movimentando cada chão ao mesmo tempo
        self.x -= self.SPEED
        self.x1 -= self.SPEED
        
        # Se um dos chãos sair pra fora da tela, são movidos para o começo da tela a direita
        if self.x <= 0 - self.IMG.get_width():
            self.x = self.WIDTH_FLOOR
        elif self.x1 <= 0 - self.IMG.get_width():
            self.x1 = self.WIDTH_FLOOR
    
    # Função que desenha cada chão
    def draw(self, screen):
        screen.blit(self.IMG, (self.x, self.y))
        screen.blit(self.IMG, (self.x1, self.y))