import pygame
import pygame.freetype 
import random
from items import ITEMS
from enemies import ENEMIES, BOSSES
from battle_actions import Battle

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

FONT = pygame.freetype.Font(None, 16)  

try:
    with open('save.txt', 'r') as f:
        max_score = int(f.readline().strip())
        last_score = int(f.readline().strip())
except (FileNotFoundError, ValueError):
    max_score = 0
    last_score = 0


def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        width, _ = font.get_rect(test_line).size
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines
def remove_unique_items(allowed_items):
    if "magic_attack" in player.actions: 
        magic_tome = [d for d in ITEMS if d.get('name') == 'Magic Tome']
        if magic_tome != []:
            if magic_tome[0] in allowed_items:
                allowed_items.remove(magic_tome[0])
    return allowed_items

class Character:
    def __init__(self, hp=1, atk=1, magic=1, actions=None, statuses=None):
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.magic = magic
        self.gold = 0
        self.actions = actions if actions is not None else []
        self.statuses = statuses if statuses is not None else []


class Button:
    def __init__(self, width, height, text, action=None):
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.clicked = False

    def draw(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        hover = (x < mouse[0] < x + self.width) and (y < mouse[1] < y + self.height)
        color = (23, 204, 58) if hover else (13, 162, 58)
        pygame.draw.rect(screen, color, (x, y, self.width, self.height))

        if hover and click[0] == 1 and not self.clicked and self.action is not None:
            self.action()
            self.clicked = True
        elif click[0] == 0:
            self.clicked = False

        padding = 5
        max_text_width = self.width - 2 * padding
        lines = wrap_text(self.text, FONT, max_text_width)

        line_height = FONT.get_sized_height()
        total_text_height = len(lines) * line_height
        start_y = y + (self.height - total_text_height) // 2

        for i, line in enumerate(lines):
            text_surface, rect = FONT.render(line, (255, 255, 255))
            text_x = x + (self.width - rect.width) // 2
            text_y = start_y + i * line_height
            screen.blit(text_surface, (text_x, text_y))

class GameState:
    def __init__(self, state='Menu'):
        self.state = state

gamestate = GameState()
player = Character(hp=5, atk=3, magic=1, actions=["slash", "heal"])
enemy = None
score = 0
difficulty = 0
boss_difficulty = 0
game_running = True
phase_running = True

# --- Функции кнопок ---
def reset_action():
    global score, difficulty, boss_difficulty
    player.max_hp = 5
    player.hp = player.max_hp
    player.atk = 3
    player.magic = 1
    player.gold = 0
    player.actions = ["slash", "heal"]
    score, difficulty, boss_difficulty = 0, 0, -1

def start_game_action():
    global phase_running
    reset_action()
    gamestate.state = 'Battle'
    phase_running = False
    wait_for_release()

def start_battle_action():
    global phase_running
    gamestate.state = 'Battle'
    enemy.max_hp = round(enemy.max_hp * (1.2 ** difficulty))
    enemy.hp = enemy.max_hp
    phase_running = False
    wait_for_release()

def wait_for_release():
    while pygame.mouse.get_pressed()[0]:
        pygame.event.pump()
        clock.tick(60)

def apply_effect(item, player):
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
        multiplier = 1.2 ** difficulty
    else:
        enemy_data = random.choice(BOSSES)
        multiplier = 1 * (1.2 ** boss_difficulty)
    hp = int(enemy_data["base_hp"] * multiplier)
    atk = int(enemy_data["base_atk"] * multiplier) or 1
    actions = enemy_data["actions"]
    return Character(hp=hp, atk=atk, actions=actions)

# --- Отрисовка ---
def draw_player(x, y, size=50):
    cube_color = (100, 150, 200)
    pygame.draw.rect(screen, cube_color, (x, y, size, size))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, size, size), 2)

    bar_width = size
    bar_height = 5
    bar_x = x
    bar_y = y - 10
    pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    hp_percentage = player.hp / player.max_hp
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percentage, bar_height))

    hp_text = f"HP: {player.hp}/{player.max_hp}"
    atk_text = f"ATK: {player.atk}"
    hp_surface, hp_rect = FONT.render(hp_text, (255, 255, 255))
    atk_surface, atk_rect = FONT.render(atk_text, (255, 255, 255))

    hp_x = x + (size // 2) - (hp_rect.width // 2)
    hp_y = y + size + 5
    atk_x = x + (size // 2) - (atk_rect.width // 2)
    atk_y = hp_y + hp_rect.height + 2

    screen.blit(hp_surface, (hp_x, hp_y))
    screen.blit(atk_surface, (atk_x, atk_y))

def draw_enemy(x, y, enemy_color, size=50):
    pygame.draw.rect(screen, enemy_color, (x, y, size, size))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, size, size), 2)

    bar_width = size
    bar_height = 5
    bar_x = x
    bar_y = y - 10
    pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    hp_percentage = enemy.hp / enemy.max_hp
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_percentage, bar_height))

    hp_text = f"HP: {enemy.hp}/{enemy.max_hp}"
    atk_text = f"ATK: {enemy.atk}"
    hp_surface, hp_rect = FONT.render(hp_text, (255, 255, 255))
    atk_surface, atk_rect = FONT.render(atk_text, (255, 255, 255))

    hp_x = x + (size // 2) - (hp_rect.width // 2)
    hp_y = y + size + 5
    atk_x = x + (size // 2) - (atk_rect.width // 2)
    atk_y = hp_y + hp_rect.height + 2

    screen.blit(hp_surface, (hp_x, hp_y))
    screen.blit(atk_surface, (atk_x, atk_y))

# --- Игровые сцены ---
def battle():
    global phase_running, game_running, score, enemy, difficulty, boss_difficulty, score, max_score, last_score
    enemy = create_enemy()
    battle_instance = Battle(player, enemy, clock)

    buttons = []
    button_width, button_height = 100, 50
    start_x = 100
    spacing = 150
    y = 300

    for i, action_name in enumerate(player.actions):
        label = action_name.replace("_", " ").capitalize()
        btn = Button(button_width, button_height, label, getattr(battle_instance, action_name))
        x = start_x + i * spacing
        buttons.append((btn, x, y))

    while phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                phase_running = False
                game_running = False

        screen.fill((20, 20, 20))

        draw_player(150, 150, size=60)
        draw_enemy(390, 150, enemy_data['color'], size=60)

        for btn, x, y in buttons:
            btn.draw(x, y)

        pygame.display.update()
        clock.tick(60)

        if player.hp <= 0:
            last_score = score 
            if score > max_score:
                max_score = score
            with open('save.txt', 'w') as f:
                f.write(f"{max_score}\n{last_score}")
            gamestate.state = 'Menu'
            phase_running = False
        elif enemy.hp <= 0:
            player.gold += enemy_data["reward"]
            score += 1
            difficulty += 1
            if not (score % 4 != 0 or score == 0):
                boss_difficulty += 1
            gamestate.state = 'Shop'
            phase_running = False

def menu():
    global phase_running, game_running
    start_button = Button(100, 50, "Start game", start_game_action)

    while phase_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                phase_running = False
                game_running = False

        screen.fill((20, 20, 20))

        max_score_surf, max_score_rect = FONT.render(f"Max Score: {int(max_score)}", (255, 255, 255))
        last_score_surf, last_score_rect = FONT.render(f"Last Score: {int(last_score)}", (255, 255, 255))

        screen.blit(max_score_surf, (250, 100))
        screen.blit(last_score_surf, (250, 120))
        
        start_button.draw(250, 260)
        pygame.display.update()
        clock.tick(60)

def shop():
    global phase_running, game_running

    reroll_price = 2
    current_items = []

    def update_item_list(index=None, amount=None):
        nonlocal current_items
        allowed_items = ITEMS
        allowed_items = remove_unique_items(allowed_items)
        if len(current_items) == 0:
                current_items = random.sample(allowed_items, 3)
        if index != None:
            new_item = random.choice(allowed_items)
            current_items[index] = new_item
        if amount == 3:
            current_items = random.sample(allowed_items, 3)

    def update_item_buttons():
        nonlocal item_buttons
        item_buttons = []
        start_x = 50
        start_y = 150
        spacing = 175
        for i, item in enumerate(current_items):
            btn = Button(100, 50, f"{item['name']} ({item['price']}g)", lambda idx=i: buy_item(idx))
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
            update_item_list(index=index)
            update_item_buttons()
            wait_for_release()
        else:
            print(f"Not enough gold! Need {item['price']}, have {player.gold}")

    def reroll_action():
        nonlocal current_items
        if player.gold >= reroll_price:
            player.gold -= reroll_price
            update_item_list(amount=3)
            update_item_buttons()
            wait_for_release()
        else:
            print(f"Not enough gold to reroll! Need {reroll_price}")


    continue_button = Button(100, 50, "Next battle", start_battle_action)
    reroll_button = Button(100, 50, f"Reroll ({reroll_price}g)", reroll_action)

    
    update_item_list()
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

        reroll_button.draw(50, 300)
        continue_button.draw(400, 300)

        gold_surf, gold_rect = FONT.render(f"Gold: {player.gold}", (255, 255, 0))
        hp_surf, hp_rect = FONT.render(f"HP: {player.hp}/{player.max_hp}", (255, 255, 255))
        atk_surf, atk_rect = FONT.render(f"ATK: {player.atk}", (255, 255, 255))
        magic_surf, magic_rect = FONT.render(f"MAGIC: {player.magic}", (255, 255, 255))

        screen.blit(gold_surf, (10, 10))
        screen.blit(hp_surf, (500, 10))
        screen.blit(atk_surf, (500, 30))
        screen.blit(magic_surf, (500, 50))

        pygame.display.update()
        clock.tick(60)

# --- Игровой цикл ---
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