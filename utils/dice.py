import random

def roll_dice(sides: int = 6) -> int:
    """Бросок кубика с указанным количеством сторон"""
    return random.randint(1, sides)

def roll_stats() -> tuple[int, int, int]:
    """Генерация случайных характеристик персонажа"""
    return (
        random.randint(1, 3),  # Сила
        random.randint(1, 3),  # Ловкость
        random.randint(1, 3)   # Выносливость
    )