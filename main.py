import pygame
import random  
from items import ITEMS
from enemies import ENEMIES, BOSSES
from battle_actions import Battle

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

class Character:
    def __init__(self, hp=1, atk=1, magic=1, actions=[]):
        self.hp = hp
        self.max_hp = hp  
        self.atk = atk
        self.magic = magic
        self.gold = 0 
        self.actions = actions  

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

player = Character(hp=5, atk=3, magic=1, actions=["slash", "heal"])
enemy = None
global phase_running, game_running, score
score = 0
game_running = True
phase_running = True

font = pygame.font.Font(None, 24)  

# --- Действия для кнопок ---
def reset_action():
    global score
    player.max_hp = 5
    player.hp = player.max_hp
    player.atk = 3
    player.magic = 1
    player.gold = 0
    player.actions = ["slash", "heal"]
    score = 0

def start_game_action():
    global phase_running
    reset_action()
    gamestate.state = 'Battle'
    phase_running = False
    wait_for_release()

def start_battle_action():
    global phase_running
    gamestate.state = 'Battle'
    enemy.max_hp = round(enemy.max_hp * (1.2 ** score))
    enemy.hp = enemy.max_hp
    phase_running = False
    wait_for_release()

def wait_for_release():
    while pygame.mouse.get_pressed()[0]:
        pygame.event.pump()
        clock.tick(60)
# ------------------------------------

# --- Служебные функции ---
def apply_effect(item,player):
    if item['effect'] == "hp_up":
        player.max_hp += 2
        player.hp += 2
    elif item['effect'] == "atk_up":
        player.atk += 1
    elif item['effect'] == "full_heal":
        player.hp = player.max_hp
    elif item['effect'] == "magic_up":
        player.magic += 1
    elif item['effect'] == "unlock_magic_attack":
        if "magic_attack" not in player.actions:
            player.actions.append("magic_attack")


def create_enemy():
    global enemy_data
    if score % 4 != 0 or score == 0:
        enemy_data = random.choice(ENEMIES)
        multiplier = 1.2 ** score
    elif score % 4 == 0:
        enemy_data = random.choice(BOSSES)
        multiplier = 1
    hp = int(enemy_data["base_hp"] * multiplier)
    atk = int(enemy_data["base_atk"] * multiplier) or 1 
    actions = enemy_data["actions"]
    return Character(hp=hp, atk=atk, actions=actions)

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

def draw_enemy(x, y, enemy_color, size=50):
    color =  enemy_color
    pygame.draw.rect(screen, color, (x, y, size, size))
    
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
    global phase_running, game_running, score, enemy

    enemy = create_enemy()

    battle_instance = Battle(player, enemy, clock)

    buttons = []  
    button_width, button_height = 100, 50
    start_x = 100
    spacing = 150
    y = 300

    for i, action_name in enumerate(player.actions):
        if hasattr(battle_instance, action_name):
            btn = Button(button_width, button_height, action=getattr(battle_instance, action_name))
            x = start_x + i * spacing
            buttons.append((btn, x, y, action_name))


    while phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                phase_running = False
                game_running = False
        
        screen.fill((20, 20, 20))

        draw_player(150, 150, size=60)
        draw_enemy(390, 150, enemy_data['color'], size=60)  
        
        for btn, x, y, label in buttons:
            btn.draw(x, y)
            text = font.render(label.replace("_", " ").capitalize(), True, (255, 255, 255))
            screen.blit(text, (x, y - 20))

        pygame.display.update()
        clock.tick(60)

        if player.hp <= 0:
            gamestate.state = 'Menu'
            phase_running = False
        elif enemy.hp <= 0:
            player.gold += enemy_data["reward"]
            score += 1
            print(score)
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

        start_button.draw(250, 260)

        label = font.render("Start game", True, (255, 255, 255))
        screen.blit(label, (250, 240))

        pygame.display.update()
        clock.tick(60)

def shop():
    global phase_running, game_running

    reroll_price = 2
    current_items = random.sample(ITEMS, 3)
    
    def update_item_buttons():
        nonlocal item_buttons
        item_buttons = []
        start_x = 50
        start_y = 150
        spacing = 175
        for i, item in enumerate(current_items):
            btn = Button(100, 50, action=lambda idx=i: buy_item(idx))
            item_buttons.append({
                "button": btn,
                "x": start_x + i * spacing,
                "y": start_y,
                "name": item["name"],
                "price": item["price"]
            })

    def buy_item(index):
        item = current_items[index]
        if player.gold >= item["price"]:
            player.gold -= item["price"]
            apply_effect(item, player)
            new_item = random.choice(ITEMS)
            current_items[index] = new_item
            update_item_buttons()
            print(f"Куплено: {item['name']}. Осталось золота: {player.gold}")
            wait_for_release()
        else:
            print(f"Не хватает золота! Нужно: {item['price']}, у вас: {player.gold}")

    def reroll_action():
        nonlocal current_items
        if player.gold >= reroll_price:
            player.gold -= reroll_price
            current_items = random.sample(ITEMS, 3)
            update_item_buttons()
            print(f"Reroll! Новые предметы. Золото: {player.gold}")
            wait_for_release()
        else:
            print(f"Не хватает золота для reroll! Нужно: {reroll_price}")

    continue_button = Button(100, 50, action=start_battle_action)
    reroll_button = Button(100, 50, action=reroll_action)

    item_buttons = []
    update_item_buttons()

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

        reroll_button.draw(50, 300)
        reroll_text = font.render(f"Reroll ({reroll_price} gold)", True, (255, 255, 255))
        screen.blit(reroll_text, (50, 280))

        continue_button.draw(400, 300)
        continue_label = font.render("next battle", True, (255, 255, 255))
        screen.blit(continue_label, (400, 280))

        gold_text = font.render(f"Gold: {player.gold}", True, (255, 255, 0))
        screen.blit(gold_text, (10, 10))

        hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, (255, 255, 255))
        atk_text = font.render(f"ATK: {player.atk}", True, (255, 255, 255))
        magic_text = font.render(f"MAGIC: {player.magic}", True, (255, 255, 255))

        screen.blit(hp_text, (500, 10))
        screen.blit(atk_text, (500, 30))
        screen.blit(magic_text, (500, 50))

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