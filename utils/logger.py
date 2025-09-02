def log(message: str) -> None:
    """Простая функция логирования"""
    print(message)

def battle_log(message: str) -> None:
    """Лог для боевых сообщений"""
    print(f"{message}")

def game_log(message: str) -> None:
    """Лог для игровых сообщений"""
    print(f"{message}")

def success_log(message: str) -> None:
    """Лог для успешных действий"""
    print(f"{message}")

def error_log(message: str) -> None:
    """Лог для ошибок"""
    print(f"{message}")

def warning_log(message: str) -> None:
    """Лог для предупреждений"""
    print(f"{message}")