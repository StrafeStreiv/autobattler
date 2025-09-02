from enum import Enum
from dataclasses import dataclass

class DamageType(Enum):
    SLASHING = "Рубящий"
    BLUNT = "Дробящий"
    PIERCING = "Колющий"

@dataclass
class Weapon:
    name: str
    damage: int
    damage_type: DamageType

WEAPONS = {
    "Меч": Weapon("Меч", 3, DamageType.SLASHING),
    "Дубина": Weapon("Дубина", 3, DamageType.BLUNT),
    "Кинжал": Weapon("Кинжал", 2, DamageType.PIERCING),
    "Топор": Weapon("Топор", 4, DamageType.SLASHING),
    "Копье": Weapon("Копье", 3, DamageType.PIERCING),
    "Легендарный Меч": Weapon("Легендарный Меч", 10, DamageType.SLASHING)
}