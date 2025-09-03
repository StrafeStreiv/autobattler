import unittest
from unittest.mock import patch
from core.battle import Battle
from core.character import Character, CharacterStats
from core.enemy import Enemy
from data.classes import CharacterClass
from data.enemies import ENEMIES


class TestBattle(unittest.TestCase):

    def setUp(self):
        """Настройка тестовых персонажа и врага"""
        stats = CharacterStats(strength=3, agility=3, endurance=2)
        self.character = Character(CharacterClass.WARRIOR, stats)

        enemy_data = ENEMIES[0]  # Гоблин
        self.enemy = Enemy.from_data(enemy_data)

    def test_battle_initialization(self):
        """Тест инициализации боя"""
        battle = Battle(self.character, self.enemy)

        self.assertEqual(battle.character, self.character)
        self.assertEqual(battle.enemy, self.enemy)
        self.assertEqual(battle.turn_count, 0)

    @patch('random.randint')
    def test_hit_chance_calculation(self, mock_randint):
        """Тест расчета шанса попадания"""
        battle = Battle(self.character, self.enemy)

        # Симуляция успешного попадания
        mock_randint.return_value = 5  # 5 > 1 (ловкость гоблина)
        hit = battle._calculate_hit_chance(self.character, self.enemy, True)
        self.assertTrue(hit)

        # Симуляция промаха
        mock_randint.return_value = 1  # 1 <= 1
        hit = battle._calculate_hit_chance(self.character, self.enemy, True)
        self.assertFalse(hit)

    def test_damage_calculation(self):
        """Тест расчета урона"""
        battle = Battle(self.character, self.enemy)

        # Урон персонажа: 3 (меч) + 3 (сила) = 6
        damage = battle._calculate_damage(self.character, self.enemy, True)
        self.assertEqual(damage, 6)

        # Урон врага: 2 (оружие) + 1 (сила) = 3
        damage = battle._calculate_damage(self.enemy, self.character, False)
        self.assertEqual(damage, 3)

    def test_first_attacker_determination(self):
        """Тест определения первого атакующего"""
        battle = Battle(self.character, self.enemy)

        # Персонаж с ловкостью 3 vs враг с ловкостью 1 → персонаж первый
        attacker, defender, is_player = battle._determine_first_attacker()
        self.assertEqual(attacker, self.character)
        self.assertEqual(defender, self.enemy)
        self.assertTrue(is_player)

        # Тест с более ловким врагом
        agile_enemy_data = ENEMIES[3]  # Призрак с ловкостью 3
        agile_enemy = Enemy.from_data(agile_enemy_data)

        # Создаем персонажа с меньшей ловкостью
        weak_stats = CharacterStats(strength=1, agility=2, endurance=1)
        weak_character = Character(CharacterClass.WARRIOR, weak_stats)

        battle_with_agile = Battle(weak_character, agile_enemy)

        attacker, defender, is_player = battle_with_agile._determine_first_attacker()
        self.assertEqual(attacker, agile_enemy)
        self.assertEqual(defender, weak_character)
        self.assertFalse(is_player)

    def test_first_attacker_equal_agility(self):
        """Тест определения атакующего при равной ловкости"""
        # Создаем врага с такой же ловкостью как у персонажа
        equal_agility_enemy_data = ENEMIES[3]  # Призрак с ловкостью 3
        equal_agility_enemy = Enemy.from_data(equal_agility_enemy_data)

        # Персонаж тоже с ловкостью 3
        battle = Battle(self.character, equal_agility_enemy)

        # При равной ловкости персонаж должен ходить первым
        attacker, defender, is_player = battle._determine_first_attacker()
        self.assertEqual(attacker, self.character)
        self.assertEqual(defender, equal_agility_enemy)
        self.assertTrue(is_player)


if __name__ == '__main__':
    unittest.main()