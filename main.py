import random
from core.character import Character, CharacterStats, CharacterClass
from data.classes import CLASS_DATA
from utils.dice import roll_stats
from utils.logger import game_log


def create_character():
    """Создание нового персонажа"""
    game_log("=== СОЗДАНИЕ ПЕРСОНАЖА ===")
    game_log("Бросаем кубики для характеристик...")

    # Генерация характеристик
    strength, agility, endurance = roll_stats()
    stats = CharacterStats(strength, agility, endurance)

    game_log(f"Характеристики: Сила={strength}, Ловкость={agility}, Выносливость={endurance}")

    # Выбор класса
    game_log("Выберите класс:")
    classes = list(CharacterClass)
    for i, char_class in enumerate(classes, 1):
        class_data = CLASS_DATA[char_class]
        game_log(f"{i}. {class_data.name}")

    while True:
        try:
            choice = int(input("Ваш выбор (1-3): "))
            if 1 <= choice <= 3:
                selected_class = classes[choice - 1]
                character = Character(selected_class, stats)
                return character
            else:
                game_log("Пожалуйста, введите число от 1 до 3")
        except ValueError:
            game_log("Пожалуйста, введите корректное число")


def main():
    """Главная функция игры"""
    game_log("=== АВТОБАТТЛЕР ===")
    game_log("День 1: Система персонажей")

    # Создание персонажа
    character = create_character()

    # Вывод информации о персонаже
    game_log("Персонаж создан!")
    game_log("=" * 40)
    print(character)
    game_log("=" * 40)

    game_log("На сегодня это всё! Завтра добавим систему боя и врагов!")


if __name__ == "__main__":
    main()