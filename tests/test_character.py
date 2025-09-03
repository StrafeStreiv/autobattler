import unittest
from core.character import Character, CharacterStats
from data.classes import CharacterClass


class TestCharacter(unittest.TestCase):

    def setUp(self):
        """Настройка тестового персонажа"""
        stats = CharacterStats(strength=2, agility=3, endurance=1)
        self.character = Character(CharacterClass.ROGUE, stats)

    def test_character_creation(self):
        """Тест создания персонажа"""
        self.assertEqual(self.character.stats.strength, 2)
        self.assertEqual(self.character.stats.agility, 3)
        self.assertEqual(self.character.stats.endurance, 1)
        self.assertEqual(self.character.level, 1)
        self.assertEqual(self.character.character_class, CharacterClass.ROGUE)

    def test_max_health_calculation(self):
        """Тест расчета максимального здоровья"""
        # Разбойник: 4 HP за уровень + 1 от выносливости = 5
        self.assertEqual(self.character.max_health, 5)

        # Проверка другого класса
        stats = CharacterStats(strength=1, agility=1, endurance=2)
        warrior = Character(CharacterClass.WARRIOR, stats)
        # Воин: 5 HP за уровень + 2 от выносливости = 7
        self.assertEqual(warrior.max_health, 7)

    def test_starting_weapon(self):
        """Тест стартового оружия"""
        self.assertEqual(self.character.weapon.name, "Кинжал")
        self.assertEqual(self.character.weapon.damage, 2)

        # Проверяем воина
        stats = CharacterStats(strength=1, agility=1, endurance=1)
        warrior = Character(CharacterClass.WARRIOR, stats)
        self.assertEqual(warrior.weapon.name, "Меч")

    def test_level_up(self):
        """Тест повышения уровня"""
        initial_health = self.character.max_health

        # Повышаем уровень разбойника
        self.character.level_up(CharacterClass.ROGUE)

        self.assertEqual(self.character.level, 2)
        self.assertEqual(self.character.class_levels[CharacterClass.ROGUE], 2)
        self.assertEqual(self.character.stats.agility, 4)  # +1 к ловкости
        self.assertGreater(self.character.max_health, initial_health)

    def test_multiclass(self):
        """Тест мультикласса"""
        self.character.level_up(CharacterClass.WARRIOR)

        self.assertEqual(self.character.level, 2)
        self.assertEqual(self.character.class_levels[CharacterClass.ROGUE], 1)
        self.assertEqual(self.character.class_levels[CharacterClass.WARRIOR], 1)
        self.assertEqual(self.character.stats.strength, 2)  # Не должно измениться


if __name__ == '__main__':
    unittest.main()