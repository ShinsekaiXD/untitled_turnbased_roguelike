import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

class Character:
    def __init__(self, hp, atk):
        self.hp = hp
        self.max_hp = hp  
        self.atk = atk

class Button:
    def __init__(self, width, height, action=None):
        self.width = width
        self.height = height
        self.action = action
        self.clicked = False

    def draw(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if (x < mouse[0] < x + self.width) and (y < mouse[1] < y + self.height):
            pygame.draw.rect(screen, (23, 204, 58), (x, y, self.width, self.height))
            
            if click[0] == 1 and not self.clicked and self.action != None:
                self.action()
                self.clicked = True
            elif click[0] == 0:
                self.clicked = False
        else:
            pygame.draw.rect(screen, (13, 162, 58), (x, y, self.width, self.height))
            self.clicked = False

player = Character(hp=5, atk=3)

font = pygame.font.Font(None, 24)  

def attack_action():
    player.hp = max(0, player.hp - 1)
    print(f"Player HP: {player.hp}/{player.max_hp}")

def heal_action():
    player.hp = min(player.max_hp, player.hp + 1)  
    print(f"Player HP: {player.hp}/{player.max_hp}")

def reset_action():
    player.hp = player.max_hp  
    print(f"Reset. HP: {player.hp}/{player.max_hp}")

def draw_player(x, y, size=50):
    
    cube_color = (100, 150, 200)  
    pygame.draw.rect(screen, cube_color, (x, y, size, size))
    
    pygame.draw.rect(screen, (255, 255, 255), (x, y, size, size), 2)
    
    hp_text = f"HP: {player.hp}/{player.max_hp}"
    atk_text = f"ATK: {player.atk}"
    
    hp_surface = font.render(hp_text, True, (255, 255, 255))  
    atk_surface = font.render(atk_text, True, (255, 255, 255))
    
    hp_x = x + (size // 2) - (hp_surface.get_width() // 2)
    hp_y = y + size + 5
    atk_x = x + (size // 2) - (atk_surface.get_width() // 2)
    atk_y = hp_y + hp_surface.get_height() + 2

    screen.blit(hp_surface, (hp_x, hp_y))
    screen.blit(atk_surface, (atk_x, atk_y))
    
    bar_width = size
    bar_height = 5
    bar_x = x
    bar_y = y - 10
    
    pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))

    hp_percentage = player.hp / player.max_hp
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percentage, bar_height))

def game_state():
    is_running = True
    
    attack_button = Button(100, 50, action=attack_action)
    heal_button = Button(100, 50, action=heal_action)
    reset_button = Button(100, 50, action=reset_action)
    
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        
        screen.fill((20, 20, 20))

        draw_player(150, 150, size=60)

        attack_button.draw(100, 300)
        heal_button.draw(250, 300)
        reset_button.draw(400, 300)

        attack_label = font.render("Attack", True, (255, 255, 255))
        heal_label = font.render("Heal", True, (255, 255, 255))
        reset_label = font.render("Reset", True, (255, 255, 255))
        
        screen.blit(attack_label, (100, 280))
        screen.blit(heal_label, (250, 280))
        screen.blit(reset_label, (400, 280))
        
        pygame.display.update()
        clock.tick(60)

game_state()