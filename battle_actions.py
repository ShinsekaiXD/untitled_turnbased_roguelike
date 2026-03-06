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
    
    def _wait_for_release(self):
        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()
            self.clock.tick(60)