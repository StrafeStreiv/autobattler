from dataclasses import dataclass
from typing import Dict
from data.classes import CharacterClass, CLASS_DATA
from data.weapons import WEAPONS


@dataclass
class CharacterStats:
    strength: int
    agility: int
    endurance: int


class Character:
    def __init__(self, character_class: CharacterClass, stats: CharacterStats):
        self.character_class = character_class
        self.stats = stats
        self.level = 1
        self.class_levels: Dict[CharacterClass, int] = {character_class: 1}
        self.weapon = self._get_starting_weapon()
        self.max_health = self._calculate_max_health()
        self.health = self.max_health
        self.turn_count = 0
        self.battle_effects = {}

    def _get_starting_weapon(self):
        class_data = CLASS_DATA[self.character_class]
        return WEAPONS[class_data.starting_weapon]

    def _calculate_max_health(self) -> int:
        total_health = 0
        for char_class, level in self.class_levels.items():
            class_data = CLASS_DATA[char_class]
            total_health += class_data.health_per_level * level
        return total_health + self.stats.endurance

    def get_class_name(self) -> str:
        class_names = []
        for char_class, level in self.class_levels.items():
            class_data = CLASS_DATA[char_class]
            class_names.append(f"{class_data.name} {level}")
        return " / ".join(class_names)

    def level_up(self, new_class: CharacterClass):
        """Повышение уровня персонажа"""
        self.level += 1

        if new_class in self.class_levels:
            self.class_levels[new_class] += 1
        else:
            self.class_levels[new_class] = 1

        # Применяем бонусы уровня
        current_level = self.class_levels[new_class]
        if current_level == 2:
            if new_class == CharacterClass.ROGUE:
                self.stats.agility += 1
            elif new_class == CharacterClass.WARRIOR:
                self.stats.strength += 1
            elif new_class == CharacterClass.BARBARIAN:
                self.stats.endurance += 1

        self.max_health = self._calculate_max_health()
        self.health = self.max_health

    def get_class_bonuses(self) -> list:
        """Получить список активных бонусов"""
        bonuses = []
        for char_class, level in self.class_levels.items():
            class_data = CLASS_DATA[char_class]
            for lvl in range(1, level + 1):
                if lvl in class_data.level_bonuses:
                    bonuses.append(f"{class_data.name} {lvl}: {class_data.level_bonuses[lvl]}")
        return bonuses

    def apply_attack_effects(self, base_damage: int, defender_agility: int) -> int:
        """Применить эффекты атаки"""
        damage = base_damage

        # Бонусы разбойника
        if (CharacterClass.ROGUE in self.class_levels and
                self.class_levels[CharacterClass.ROGUE] >= 1 and
                self.stats.agility > defender_agility):
            damage += 1  # Скрытая атака

        # Бонусы варвара
        if CharacterClass.BARBARIAN in self.class_levels:
            barb_level = self.class_levels[CharacterClass.BARBARIAN]
            if barb_level >= 1:
                if self.turn_count <= 3:
                    damage += 2  # Ярость
                else:
                    damage -= 1  # Ярость (после 3 ходов)

        # Бонусы воина
        if (CharacterClass.WARRIOR in self.class_levels and
                self.class_levels[CharacterClass.WARRIOR] >= 1 and
                self.turn_count == 1):
            damage += self.weapon.damage  # Порыв к действию

        return max(0, damage)

    def apply_defense_effects(self, incoming_damage: int, attacker_strength: int) -> int:
        """Применить эффекты защиты"""
        damage = incoming_damage

        # Бонусы воина
        if (CharacterClass.WARRIOR in self.class_levels and
                self.class_levels[CharacterClass.WARRIOR] >= 2 and
                self.stats.strength > attacker_strength):
            damage = max(0, damage - 3)  # Щит

        # Бонусы варвара
        if (CharacterClass.BARBARIAN in self.class_levels and
                self.class_levels[CharacterClass.BARBARIAN] >= 2):
            damage = max(0, damage - self.stats.endurance)  # Каменная кожа

        return damage

    def __str__(self) -> str:
        return (f"{self.get_class_name()} (Уровень {self.level})\n"
                f"Здоровье: {self.health}/{self.max_health}\n"
                f"Сила: {self.stats.strength} | "
                f"Ловкость: {self.stats.agility} | "
                f"Выносливость: {self.stats.endurance}\n"
                f"Оружие: {self.weapon.name} ({self.weapon.damage} урона)")