import pygame

pygame.init()

class Character:
    def __init__(self,hp,atk):
        self.hp = hp
        self.atk = atk

pygame.display.set_mode((600,400))

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False