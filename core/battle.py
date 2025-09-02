import random
from typing import Optional, Tuple
from core.character import Character
from core.enemy import Enemy
from utils.logger import battle_log


class Battle:
    def __init__(self, character: Character, enemy: Enemy):
        self.character = character
        self.enemy = enemy
        self.turn_count = 0

    def execute(self) -> bool:
        """Провести бой, возвращает True если персонаж победил"""
        battle_log(f"\n=== БОЙ С {self.enemy.name.upper()} ===")
        battle_log(f"Противник: {self.enemy}")

        # Сброс счетчика ходов персонажа
        self.character.turn_count = 0

        # Определение порядка хода
        attacker, defender, attacker_is_player = self._determine_first_attacker()
        battle_log(f"{'Вы' if attacker_is_player else self.enemy.name} атакуете первым!")

        # Основной цикл боя
        while self.character.health > 0 and self.enemy.health > 0:
            self.turn_count += 1
            self.character.turn_count += 1
            battle_log(f"\n--- Ход {self.turn_count} ---")

            # Атака текущего атакующего
            damage = self._execute_attack(attacker, defender, attacker_is_player)

            if damage is not None and damage > 0:
                defender.health -= damage
                battle_log(f"{attacker.name if not attacker_is_player else 'Вы'} наносите {damage} урона!")

                # Проверка конца боя
                if defender.health <= 0:
                    defender.health = 0
                    battle_log(f"{defender.name if not attacker_is_player else 'Вы'} побеждены!")
                    break

            # Показ здоровья
            battle_log(f"Ваше здоровье: {self.character.health}/{self.character.max_health}")
            battle_log(f"Здоровье {self.enemy.name}: {self.enemy.health}/{self.enemy.max_health}")

            # Смена атакующего и защищающегося
            attacker, defender, attacker_is_player = defender, attacker, not attacker_is_player

        return self.character.health > 0

    def _determine_first_attacker(self) -> Tuple:
        if self.character.stats.agility >= self.enemy.agility:
            return self.character, self.enemy, True
        else:
            return self.enemy, self.character, False

    def _execute_attack(self, attacker, defender, attacker_is_player: bool) -> Optional[int]:
        # Проверка попадания
        hit_chance = self._calculate_hit_chance(attacker, defender, attacker_is_player)
        if not hit_chance:
            battle_log(f"{attacker.name if not attacker_is_player else 'Вы'} промахнулись!")
            return None

        # Расчет урона
        damage = self._calculate_damage(attacker, defender, attacker_is_player)
        return max(0, damage)

    def _calculate_hit_chance(self, attacker, defender, attacker_is_player: bool) -> bool:
        attacker_agi = attacker.stats.agility if attacker_is_player else attacker.agility
        defender_agi = defender.stats.agility if not attacker_is_player else defender.agility

        random_num = random.randint(1, attacker_agi + defender_agi)
        return random_num > defender_agi

    def _calculate_damage(self, attacker, defender, attacker_is_player: bool) -> int:
        if attacker_is_player:
            base_damage = self.character.weapon.damage + self.character.stats.strength
        else:
            base_damage = self.enemy.weapon_damage + self.enemy.strength

        # Здесь будут добавляться эффекты и особенности
        # Пока возвращаем базовый урон
        return base_damage