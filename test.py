import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
class Character:
    def __init__(self, hp, atk):
        self.hp = hp
        self.atk = atk

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + self.width) and (y < mouse[1] < y + self.height):
            pygame.draw.rect(screen, (23, 204, 58), (x, y, self.width, self.height))
                
            if click[0] == 1 and action != None:
                print("Button pressed")
                action()

        else:
            pygame.draw.rect(screen, (13, 162, 58), (x, y, self.width, self.height))
        



def game_state():
    is_running = True
    button = Button(100, 50)
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        screen.fill((20, 20, 20))
        button.draw(20, 100)
        pygame.display.update()
        clock.tick(60)

game_state()