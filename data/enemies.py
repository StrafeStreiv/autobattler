from dataclasses import dataclass
from typing import List

@dataclass
class EnemyData:
    name: str
    health: int
    weapon_damage: int
    strength: int
    agility: int
    endurance: int
    features: str
    reward: str

ENEMIES: List[EnemyData] = [
    EnemyData("Гоблин", 5, 2, 1, 1, 1, "Нет особых способностей", "Кинжал"),
    EnemyData("Скелет", 10, 2, 2, 2, 1,
             "Уязвим к дробящему оружию (удвоенный урон)", "Дубина"),
    EnemyData("Слайм", 8, 1, 3, 1, 2,
             "Невосприимчив к рубящему оружию", "Копье"),
    EnemyData("Призрак", 6, 3, 1, 3, 1,
             "Скрытая атака (+1 урон при превосходстве в ловкости)", "Меч"),
    EnemyData("Голем", 10, 1, 3, 1, 3,
             "Каменная кожа (снижение урона на значение выносливости)", "Топор"),
    EnemyData("Дракон", 20, 4, 3, 3, 3,
             "Дыхание огнём (+3 урона каждый 3-й ход)", "Легендарный Меч")
]