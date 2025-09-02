from dataclasses import dataclass
from typing import Dict
from ..data.classes import CharacterClass, CLASS_DATA
from ..data.weapons import WEAPONS


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
        return CLASS_DATA[self.character_class].name

    def __str__(self) -> str:
        return (f"{self.get_class_name()} (Уровень {self.level})\n"
                f"Здоровье: {self.health}/{self.max_health}\n"
                f"Сила: {self.stats.strength} | "
                f"Ловкость: {self.stats.agility} | "
                f"Выносливость: {self.stats.endurance}\n"
                f"Оружие: {self.weapon.name} ({self.weapon.damage} урона)")