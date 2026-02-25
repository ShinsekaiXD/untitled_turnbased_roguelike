import pygame
from functools import partial  

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

class Character:
    def __init__(self, hp=99, atk=99):
        self.hp = hp
        self.max_hp = hp  
        self.atk = atk
        self.gold = 0  

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

class state:
    def __init__(self,state='Menu'):
        self.state = state

gamestate = state()

player = Character(hp=5, atk=3)
enemy = Character(hp=5, atk=1)  
global phase_running, game_running
game_running = True
phase_running = True

font = pygame.font.Font(None, 24)  

# --- Действия для кнопок ---
def attack_action():
    enemy.hp = max(0, enemy.hp - player.atk)
    print(f"Enemy HP: {enemy.hp}/{enemy.max_hp}")
    enemy_action()

def heal_action():
    player.hp = min(player.max_hp, player.hp + 1)  
    print(f"Player HP: {player.hp}/{player.max_hp}")
    enemy_action()

def enemy_action():
    player.hp = max(0, player.hp - enemy.atk)
    print(f"Player HP: {player.hp}/{player.max_hp}")

def reset_action():
    player.max_hp = 5
    player.hp = player.max_hp
    player.atk = 3
    enemy.max_hp = 5    
    enemy.hp = enemy.max_hp
    player.gold = 0
    print(f"Reset. Player HP: {player.hp}/{player.max_hp}, Enemy HP: {enemy.hp}/{enemy.max_hp}")

def start_game_action():
    global phase_running
    reset_action()
    gamestate.state = 'Battle'
    phase_running = False

def start_battle_action():
    global phase_running
    gamestate.state = 'Battle'
    enemy.max_hp = round(enemy.max_hp * 1.2)
    enemy.hp = enemy.max_hp
    phase_running = False
# ------------------------------------

# --- Функции для покупок в магазине ---
ITEMS = [
    {
        "id": "hp_up",
        "name": "HP +2",
        "price": 5,
        "effect": lambda: player.__setattr__('max_hp', player.max_hp + 2) or player.__setattr__('hp', player.hp + 2) 
    },
    {
        "id": "atk_up",
        "name": "ATK +1",
        "price": 5,
        "effect": lambda: player.__setattr__('atk', player.atk + 1)
    },
    {
        "id": "full_heal",
        "name": "Full Heal",
        "price": 3,
        "effect": lambda: player.__setattr__('hp', player.max_hp)
    }
]

def make_buy_action(item):
    """Возвращает функцию, которая выполняет покупку указанного предмета"""
    def buy():
        if player.gold >= item["price"]:
            player.gold -= item["price"]
            item["effect"]()
            print(f"Куплено: {item['name']}. Осталось золота: {player.gold}")
        else:
            print(f"Не хватает золота! Нужно: {item['price']}, у вас: {player.gold}")
    return buy
# ------------------------------------

# --- Команды отрисовки ---
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

def draw_enemy(x, y, size=50):
    cube_color = (200, 100, 100)  
    pygame.draw.rect(screen, cube_color, (x, y, size, size))
    
    pygame.draw.rect(screen, (255, 255, 255), (x, y, size, size), 2)
    
    hp_text = f"HP: {enemy.hp}/{enemy.max_hp}"
    atk_text = f"ATK: {enemy.atk}"
    
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

    hp_percentage = enemy.hp / enemy.max_hp
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percentage, bar_height))
# ------------------------------------

# --- Сцены игры ---
def battle():
    global phase_running, game_running

    attack_button = Button(100, 50, action=attack_action)
    heal_button = Button(100, 50, action=heal_action)

    while phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                phase_running = False
                game_running = False
        
        screen.fill((20, 20, 20))

        draw_player(150, 150, size=60)
        draw_enemy(390, 150, size=60)  

        attack_button.draw(100, 300)
        heal_button.draw(250, 300)

        attack_label = font.render("Attack", True, (255, 255, 255))
        heal_label = font.render("Heal", True, (255, 255, 255))

        screen.blit(attack_label, (100, 280))
        screen.blit(heal_label, (250, 280))

        pygame.display.update()
        clock.tick(60)

        if player.hp <= 0:
            gamestate.state = 'Menu'
            phase_running = False
        elif enemy.hp <= 0:
            player.gold += 10 
            gamestate.state = 'Shop'
            phase_running = False

def menu():
    global phase_running, game_running

    start_button = Button(100, 50, action=start_game_action)

    while phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                phase_running = False
                game_running = False

        screen.fill((20, 20, 20))

        start_button.draw(200, 260)

        label = font.render("start game", True, (255, 255, 255))
        screen.blit(label, (250, 280))

        pygame.display.update()
        clock.tick(60)

def shop():
    global phase_running, game_running

    continue_button = Button(100, 50, action=start_battle_action)

    item_buttons = []
    start_x = 50
    start_y = 150
    spacing = 150  

    for i, item in enumerate(ITEMS):
        btn = Button(100, 50, action=make_buy_action(item))
        item_buttons.append({
            "button": btn,
            "x": start_x + i * spacing,
            "y": start_y,
            "name": item["name"],
            "price": item["price"]
        })

    while phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                phase_running = False
                game_running = False

        screen.fill((20, 20, 20))

        for it in item_buttons:
            it["button"].draw(it["x"], it["y"])
            text = font.render(f"{it['name']} ({it['price']} gold)", True, (255, 255, 255))
            screen.blit(text, (it["x"], it["y"] - 20))

        continue_button.draw(200, 260)
        label = font.render("next battle", True, (255, 255, 255))
        screen.blit(label, (250, 280))

        gold_text = font.render(f"Gold: {player.gold}", True, (255, 255, 0))
        screen.blit(gold_text, (10, 10))

        pygame.display.update()
        clock.tick(60)
# ------------------------------------

while game_running:    
    if gamestate.state == 'Menu':
        phase_running = True
        menu()
    elif gamestate.state == 'Battle':
        phase_running = True
        battle()
    elif gamestate.state == 'Shop':
        phase_running = True
        shop()