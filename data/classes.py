from enum import Enum
from dataclasses import dataclass
from typing import Dict

class CharacterClass(Enum):
    WARRIOR = "warrior"
    BARBARIAN = "barbarian"
    ROGUE = "rogue"

@dataclass
class ClassData:
    name: str
    health_per_level: int
    starting_weapon: str
    level_bonuses: Dict[int, str]

CLASS_DATA = {
    CharacterClass.WARRIOR: ClassData(
        name="Воин",
        health_per_level=5,
        starting_weapon="Меч",
        level_bonuses={
            1: "Порыв к действию: В первый ход наносит двойной урон оружием",
            2: "Щит: -3 к получаемому урону если сила выше атакующего",
            3: "+1 к силе"
        }
    ),
    CharacterClass.BARBARIAN: ClassData(
        name="Варвар",
        health_per_level=6,
        starting_weapon="Дубина",
        level_bonuses={
            1: "Ярость: +2 к урону в первые 3 хода, потом -1 к урону",
            2: "Каменная кожа: Получаемый урон снижается на значение выносливости",
            3: "+1 к выносливости"
        }
    ),
    CharacterClass.ROGUE: ClassData(
        name="Разбойник",
        health_per_level=4,
        starting_weapon="Кинжал",
        level_bonuses={
            1: "Скрытая атака: +1 к урону если ловкость выше цели",
            2: "+1 к ловкости",
            3: "Яд: Наносит дополнительные +1 урона на втором ходу, +2 на третьем и т.д."
        }
    )
}