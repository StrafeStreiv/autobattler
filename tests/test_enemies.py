import unittest
from core.enemy import Enemy
from data.enemies import ENEMIES
from data.weapons import WEAPONS


class TestEnemy(unittest.TestCase):

    def test_enemy_creation(self):
        """Тест создания врага из данных"""
        enemy_data = ENEMIES[0]  # Гоблин
        enemy = Enemy.from_data(enemy_data)

        self.assertEqual(enemy.name, "Гоблин")
        self.assertEqual(enemy.health, 5)
        self.assertEqual(enemy.max_health, 5)
        self.assertEqual(enemy.weapon_damage, 2)
        self.assertEqual(enemy.strength, 1)

    def test_reward_weapon(self):
        """Тест получения оружия награды"""
        enemy_data = ENEMIES[0]  # Гоблин, Кинжал
        enemy = Enemy.from_data(enemy_data)
        weapon = enemy.get_reward_weapon()

        self.assertEqual(weapon.name, "Кинжал")
        self.assertEqual(weapon.damage, 2)

    def test_all_enemies_have_valid_rewards(self):
        """Тест что у всех врагов есть валидные награды"""
        for enemy_data in ENEMIES:
            enemy = Enemy.from_data(enemy_data)
            weapon = enemy.get_reward_weapon()
            self.assertIsNotNone(weapon)
            self.assertIn(weapon.name, WEAPONS.keys())


class TestWeapons(unittest.TestCase):

    def test_weapon_properties(self):
        """Тест свойств оружия"""
        sword = WEAPONS["Меч"]
        self.assertEqual(sword.name, "Меч")
        self.assertEqual(sword.damage, 3)
        self.assertEqual(sword.damage_type.value, "Рубящий")

    def test_weapon_comparison(self):
        """Тест сравнения оружия"""
        dagger = WEAPONS["Кинжал"]
        sword = WEAPONS["Меч"]
        legendary = WEAPONS["Легендарный Меч"]

        self.assertLess(dagger.damage, sword.damage)
        self.assertLess(sword.damage, legendary.damage)


if __name__ == '__main__':
    unittest.main()