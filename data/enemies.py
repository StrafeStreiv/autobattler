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
    EnemyData("Гоблин", 5, 2, 1, 1, 1, "", "Кинжал"),
    EnemyData("Скелет", 10, 2, 2, 2, 1,
             "Получает вдвое больше урона от дробящего оружия", "Дубина"),
    EnemyData("Слайм", 8, 1, 3, 1, 2,
             "Рубящее оружие не наносит урона", "Копье"),
    EnemyData("Призрак", 6, 3, 1, 3, 1,
             "Скрытая атака: +1 к урону если ловкость выше цели", "Меч"),
    EnemyData("Голем", 10, 1, 3, 1, 3,
             "Каменная кожа: Получаемый урон снижается на значение выносливости", "Топор"),
    EnemyData("Дракон", 20, 4, 3, 3, 3,
             "Каждый 3-й ход дышит огнём (+3 урона)", "Легендарный Меч")
]