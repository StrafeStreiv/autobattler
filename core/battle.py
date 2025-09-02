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
        battle_log(f"\n=== БОЙ С {self._get_enemy_name_instrumental().upper()} ===")
        battle_log(f"Противник: {self.enemy}")
        if self.enemy.features:
            battle_log(f"Особенности: {self.enemy.features}")

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
                if attacker_is_player:
                    battle_log(f"Вы наносите {damage} урона!")
                else:
                    battle_log(f"{attacker.name} наносит {damage} урона!")

                # Проверка конца боя
                if defender.health <= 0:
                    defender.health = 0
                    break

            # Показ здоровья
            battle_log(f"Ваше здоровье: {self.character.health}/{self.character.max_health}")
            battle_log(f"Здоровье {self.enemy.name}: {self.enemy.health}/{self.enemy.max_health}")

            # Смена атакующего и защищающегося
            attacker, defender, attacker_is_player = defender, attacker, not attacker_is_player

        victory = self.character.health > 0
        battle_log(f"\n{'🎉 ПОБЕДА!' if victory else '💀 ПОРАЖЕНИЕ!'}")
        return victory

    def _get_enemy_name_instrumental(self) -> str:
        """Получить имя врага в творительном падеже (с кем?)"""
        enemy_names = {
            "Гоблин": "Гоблином",
            "Скелет": "Скелетом",
            "Слайм": "Слаймом",
            "Призрак": "Призраком",
            "Голем": "Големом",
            "Дракон": "Драконом"
        }
        return enemy_names.get(self.enemy.name, self.enemy.name)

    def _determine_first_attacker(self) -> Tuple:
        if self.character.stats.agility >= self.enemy.agility:
            return self.character, self.enemy, True
        else:
            return self.enemy, self.character, False

    def _execute_attack(self, attacker, defender, attacker_is_player: bool) -> Optional[int]:
        # Проверка попадания
        hit_chance = self._calculate_hit_chance(attacker, defender, attacker_is_player)
        if not hit_chance:
            if attacker_is_player:
                battle_log("Вы промахнулись!")
            else:
                battle_log(f"{attacker.name} промахнулся!")
            return None

        # Расчет урона
        damage = self._calculate_damage(attacker, defender, attacker_is_player)

        # Применение эффектов защиты
        if attacker_is_player:
            # Персонаж атакует врага
            damage = self._apply_enemy_defense_effects(damage)
        else:
            # Враг атакует персонажа
            damage = self.character.apply_defense_effects(damage, self.enemy.strength)

        return max(0, damage)

    def _calculate_hit_chance(self, attacker, defender, attacker_is_player: bool) -> bool:
        attacker_agi = attacker.stats.agility if attacker_is_player else attacker.agility
        defender_agi = defender.stats.agility if not attacker_is_player else defender.agility

        random_num = random.randint(1, attacker_agi + defender_agi)
        return random_num > defender_agi

    def _calculate_damage(self, attacker, defender, attacker_is_player: bool) -> int:
        if attacker_is_player:
            base_damage = self.character.weapon.damage + self.character.stats.strength
            # Применяем эффекты атаки персонажа
            defender_agi = self.enemy.agility
            damage = self.character.apply_attack_effects(base_damage, defender_agi)
        else:
            base_damage = self.enemy.weapon_damage + self.enemy.strength
            damage = base_damage

            # Особенности врагов
            if self.enemy.name == "Дракон" and self.turn_count % 3 == 0:
                damage += 3  # Дыхание дракона
                battle_log("🐉 Дракон дышит огнём! +3 урона")

            if ("Скрытая атака" in self.enemy.features and
                    self.enemy.agility > self.character.stats.agility):
                damage += 1  # Скрытая атака призрака
                battle_log("👻 Призрак использует скрытую атаку! +1 урона")

        return damage

    def _apply_enemy_defense_effects(self, damage: int) -> int:
        """Применить эффекты защиты врагов"""
        if self.enemy.name == "Скелет" and self.character.weapon.damage_type.value == "Дробящий":
            damage *= 2  # Уязвимость скелета к дробящему оружию
            battle_log("💀 Скелет уязвим к дробящему оружию! Урон удвоен")

        elif self.enemy.name == "Слайм" and self.character.weapon.damage_type.value == "Рубящий":
            damage = 0  # Иммунитет слайма к рубящему оружию
            battle_log("🟢 Слайм невосприимчив к рубящему оружию! Урон блокирован")

        elif "Каменная кожа" in self.enemy.features:
            damage = max(0, damage - self.enemy.endurance)
            battle_log("🪨 Каменная кожа поглощает часть урона!")

        return damage