import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
mouse_pressed = False
mouse_pos = pygame.mouse.get_pos()


class Character:
    def __init__(self, hp, atk):
        self.hp = hp
        self.atk = atk

class Button:
    def __init__(self, width, height, action=None):
        self.width = width
        self.height = height
        self.action = action

    def draw(self, x, y):
        if (x < mouse_pos[0] < x + self.width) and (y < mouse_pos[1] < y + self.height):
            pygame.draw.rect(screen, (23, 204, 58), (x, y, self.width, self.height))
    
            if self.action != None and mouse_pressed:
                self.action()
                
        else:
            pygame.draw.rect(screen, (13, 162, 58), (x, y, self.width, self.height))

def increment():
    n = 0
    print(n)
    n += 1

def game_state():
    is_running = True
    button = Button(100, 50, increment)
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pressed == True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
                mouse_pressed == False
        screen.fill((20, 20, 20))
        button.draw(20, 100)
        pygame.display.update()
        clock.tick(60)

game_state()