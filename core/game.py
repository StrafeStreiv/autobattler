import random
from typing import Optional
from core.character import Character, CharacterStats, CharacterClass
from core.enemy import Enemy
from core.battle import Battle
from data.enemies import ENEMIES
from data.classes import CLASS_DATA, CharacterClass
from data.weapons import WEAPONS
from utils.dice import roll_stats
from utils.logger import game_log, success_log, error_log


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
                    success_log(f"Создан персонаж: {self.character}")
                    break
                else:
                    error_log("Пожалуйста, введите число от 1 до 3")
            except ValueError:
                error_log("Пожалуйста, введите корректное число")

    def _handle_victory(self, enemy: Enemy):
        """Обработка победы в бою"""
        self.victories += 1
        success_log(f"ПОБЕДА! Серия побед: {self.victories}/5")

        # Восстановление здоровья
        self.character.health = self.character.max_health
        success_log("Здоровье восстановлено!")

        # Предложение сменить оружие
        self._offer_weapon_swap(enemy)

        # Повышение уровня (если не максимальный)
        if self.character.level < 3:
            self._level_up()
        else:
            game_log("📈 Максимальный уровень достигнут!")

    def _handle_defeat(self):
        """Обработка поражения в бою"""
        error_log("ПОРАЖЕНИЕ! Создайте нового персонажа.")
        self.character = None
        self.victories = 0

    def _offer_weapon_swap(self, enemy: Enemy):
        """Предложить сменить оружие на добытое"""
        new_weapon = enemy.get_reward_weapon()
        current_weapon = self.character.weapon

        game_log(f"🎁 Добыто оружие: {new_weapon.name} ({new_weapon.damage} урона)")
        game_log(f"🗡️  Ваше текущее оружие: {current_weapon.name} ({current_weapon.damage} урона)")

        if new_weapon.damage > current_weapon.damage:
            game_log("Хотите заменить оружие? (д/н)")
            while True:
                choice = input().lower().strip()
                if choice in ['д', 'да', 'y', 'yes']:
                    self.character.weapon = new_weapon
                    success_log("Оружие заменено!")
                    break
                elif choice in ['н', 'нет', 'n', 'no']:
                    game_log("Оставляете старое оружие.")
                    break
                else:
                    error_log("Пожалуйста, введите 'д' или 'н'")
        else:
            game_log("Новое оружие не лучше текущего. Пропускаем.")

    def _level_up(self):
        """Повышение уровня персонажа"""
        game_log(f"\n⭐ === ПОВЫШЕНИЕ УРОВНЯ {self.character.level} -> {self.character.level + 1} ===")

        # Показ текущих бонусов
        bonuses = self.character.get_class_bonuses()
        if bonuses:
            game_log("Ваши текущие бонусы:")
            for bonus in bonuses:
                game_log(f"  • {bonus}")

        game_log("Выберите класс для повышения:")
        classes = list(CharacterClass)
        for i, char_class in enumerate(classes, 1):
            class_data = CLASS_DATA[char_class]
            current_level = self.character.class_levels.get(char_class, 0)
            next_bonus = class_data.level_bonuses.get(current_level + 1, "Нет бонусов")
            game_log(f"{i}. {class_data.name} (Ур. {current_level}) → {next_bonus}")

        while True:
            try:
                choice = int(input("Ваш выбор (1-3): "))
                if 1 <= choice <= 3:
                    selected_class = classes[choice - 1]
                    self.character.level_up(selected_class)

                    class_data = CLASS_DATA[selected_class]
                    new_level = self.character.class_levels[selected_class]
                    new_bonus = class_data.level_bonuses.get(new_level, "")

                    success_log(f"Теперь вы {class_data.name} уровня {new_level}!")
                    if new_bonus:
                        success_log(f"Новый бонус: {new_bonus}")
                    game_log(f"📊 Новые характеристики: {self.character}")
                    break
                else:
                    error_log("Пожалуйста, введите число от 1 до 3")
            except ValueError:
                error_log("Пожалуйста, введите корректное число")

    def _victory_sequence(self):
        """Последовательность победы в игре"""
        success_log("\n=== ПОБЕДА! ===")
        success_log("Вы победили 5 монстров подряд и прошли игру!")
        success_log("Поздравляем с завершением Автобаттлера!")
        success_log(f"Ваш финальный персонаж: {self.character.get_class_name()}")
        self.game_active = False