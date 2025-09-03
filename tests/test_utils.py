import unittest
from unittest.mock import patch
from utils.dice import roll_dice, roll_stats


class TestUtils(unittest.TestCase):

    @patch('random.randint')
    def test_roll_dice(self, mock_randint):
        """Тест броска кубика"""
        mock_randint.return_value = 4
        result = roll_dice(6)
        self.assertEqual(result, 4)
        mock_randint.assert_called_with(1, 6)

        result = roll_dice(20)
        mock_randint.assert_called_with(1, 20)

    @patch('random.randint')
    def test_roll_stats(self, mock_randint):
        """Тест генерации характеристик"""
        mock_randint.side_effect = [2, 3, 1]  # Сила, Ловкость, Выносливость
        stats = roll_stats()

        self.assertEqual(stats, (2, 3, 1))
        self.assertEqual(mock_randint.call_count, 3)
        mock_randint.assert_called_with(1, 3)


if __name__ == '__main__':
    unittest.main()