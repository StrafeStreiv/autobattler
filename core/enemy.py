from dataclasses import dataclass
from data.enemies import EnemyData
from data.weapons import Weapon, WEAPONS


@dataclass
class Enemy:
    name: str
    max_health: int
    health: int
    weapon_damage: int
    strength: int
    agility: int
    endurance: int
    features: str
    reward: str

    @classmethod
    def from_data(cls, enemy_data: EnemyData) -> 'Enemy':
        return cls(
            name=enemy_data.name,
            max_health=enemy_data.health,
            health=enemy_data.health,
            weapon_damage=enemy_data.weapon_damage,
            strength=enemy_data.strength,
            agility=enemy_data.agility,
            endurance=enemy_data.endurance,
            features=enemy_data.features,
            reward=enemy_data.reward
        )

    def get_reward_weapon(self) -> Weapon:
        return WEAPONS.get(self.reward, WEAPONS["Кинжал"])

    def __str__(self) -> str:
        features = f" | Особенности: {self.features}" if self.features else ""
        return (f"{self.name} | "
                f"HP: {self.health}/{self.max_health} | "
                f"STR: {self.strength} | "
                f"AGI: {self.agility} | "
                f"END: {self.endurance}{features}")