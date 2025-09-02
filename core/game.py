import random
from typing import Optional
from core.character import Character, CharacterStats, CharacterClass
from core.enemy import Enemy
from core.battle import Battle
from data.enemies import ENEMIES
from data.classes import CLASS_DATA
from utils.dice import roll_stats
from utils.logger import game_log


class Game:
    def __init__(self):
        self.character: Optional[Character] = None
        self.victories: int = 0
        self.game_active: bool = True

    def run(self):
        """Основной игровой цикл"""
        game_log("=== АВТОБАТТЛЕР ===")

        while self.game_active:
            if not self.character:
                self._create_character()

            if self.victories >= 5:
                self._victory_sequence()
                break

            # Создание случайного врага
            enemy_data = random.choice(ENEMIES)
            enemy = Enemy.from_data(enemy_data)

            # Проведение боя
            battle = Battle(self.character, enemy)
            victory = battle.execute()

            if victory:
                self._handle_victory(enemy)
            else:
                self._handle_defeat()

            # Пауза между боями
            if self.game_active and self.victories < 5:
                input("\nНажмите Enter для продолжения...")

    def _create_character(self):
        """Создание нового персонажа"""
        game_log("\n=== СОЗДАНИЕ ПЕРСОНАЖА ===")

        stats = CharacterStats(*roll_stats())
        game_log(f"Характеристики: Сила={stats.strength}, Ловкость={stats.agility}, Выносливость={stats.endurance}")

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
                    self.character = Character(selected_class, stats)
                    game_log(f"\nСоздан персонаж: {self.character}")
                    break
                else:
                    game_log("Пожалуйста, введите число от 1 до 3")
            except ValueError:
                game_log("Пожалуйста, введите корректное число")

    def _handle_victory(self, enemy: Enemy):
        """Обработка победы в бою"""
        self.victories += 1
        game_log(f"\n🎉 ПОБЕДА! Серия побед: {self.victories}/5")

        # Восстановление здоровья
        self.character.health = self.character.max_health
        game_log("💚 Здоровье восстановлено!")

    def _handle_defeat(self):
        """Обработка поражения в бою"""
        game_log("\n💀 ПОРАЖЕНИЕ! Создайте нового персонажа.")
        self.character = None
        self.victories = 0

    def _victory_sequence(self):
        """Последовательность победы в игре"""
        game_log("\n🎊 === ПОБЕДА! ===")
        game_log("Вы победили 5 монстров подряд и прошли игру!")
        game_log("Поздравляем! 🏆")
        self.game_active = False