import pygame
import random

class Battle:
    def __init__(self, player, enemy, clock):
        self.player = player
        self.enemy = enemy
        self.clock = clock

    def enemy_action(self):
        actions = self.enemy.actions
        if not actions:
            return
        selected_action = random.choice(actions)
        print(selected_action)
        getattr(self, selected_action)()
        self.tick_statuses()
        
    def attack(self):
        self.player.hp = max(0, self.player.hp - self.enemy.atk)
        print(f"Player HP: {self.player.hp}/{self.player.max_hp}")         

    def slash(self):
        self.enemy.hp = max(0, self.enemy.hp - self.player.atk)
        print(f"Enemy HP: {self.enemy.hp}/{self.enemy.max_hp}")
        self.enemy_action()
        self._wait_for_release()

    def heal(self):
        self.player.hp = min(self.player.max_hp, self.player.hp + self.player.magic)
        print(f"Player HP: {self.player.hp}/{self.player.max_hp}")
        self.enemy_action()
        self._wait_for_release()

    def magic_attack(self):
        self.enemy.hp = max(0, self.enemy.hp - self.player.magic)
        print(f"Enemy HP: {self.enemy.hp}/{self.enemy.max_hp}")
        self.enemy_action()
        self._wait_for_release()

    def stomp(self):
        self.player.hp = max(0, self.player.hp - (self.enemy.atk * 4))
        print(f"Player HP: {self.player.hp}/{self.player.max_hp}")  
    
    def poison(self):
        self.apply_status('player', 'poison', 3)

    def apply_status(self, target, status_name, duration):
        """Накладывает статус на указанного персонажа ('player' или 'enemy')."""
        char = self.player if target == 'player' else self.enemy
        # Найти шаблон статуса
        template = next((s for s in STATUSES if s['name'] == status_name), None)
        if not template:
            return
        # Проверить, есть ли уже такой статус
        for s in char.statuses:
            if s['name'] == status_name:
                s['count'] += duration
                return
        # Добавить новый статус (копируем, чтобы не менять глобальный шаблон)
        new_status = template.copy()
        new_status['count'] = duration
        char.statuses.append(new_status)

    def tick_statuses(self):
        """Тикает все статусы у игрока и врага."""
        # Обрабатываем статусы игрока
        for status in self.player.statuses[:]:
            self._apply_status_effect(status, 'player')
            status['count'] -= 1
            if status['count'] <= 0:
                self.player.statuses.remove(status)

        # Обрабатываем статусы врага
        for status in self.enemy.statuses[:]:
            self._apply_status_effect(status, 'enemy')
            status['count'] -= 1
            if status['count'] <= 0:
                self.enemy.statuses.remove(status)


    def _apply_status_effect(self, status, target):
        """Применяет эффект статуса к цели ('player' или 'enemy')."""
        if status['name'] == 'poison':
            damage = status.get('damage', 1)
            if target == 'player':
                self.player.hp = max(0, self.player.hp - damage)
                print(f"Poison deals {damage} damage to player. HP: {self.player.hp}")
            else:
                self.enemy.hp = max(0, self.enemy.hp - damage)
                print(f"Poison deals {damage} damage to enemy. HP: {self.enemy.hp}")

    
    def _wait_for_release(self):
        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()
            self.clock.tick(60)

STATUSES = [
    {
        "name": "poison",
        "damage": 1,
        "count": 0
    }
]