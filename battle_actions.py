import pygame

class Battle:
    def __init__(self, player, enemy, clock):
        self.player = player
        self.enemy = enemy
        self.clock = clock

    def enemy_action(self):
        self.player.hp = max(0, self.player.hp - self.enemy.atk)
        print(f"Player HP: {self.player.hp}/{self.player.max_hp}")

    def attack(self):
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

    def _wait_for_release(self):
        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()
            self.clock.tick(60)