"""
Задача 28. Простая ролевая боевая система — ООП-СТИЛЬ

Состояние персонажа инкапсулировано внутри класса Character, а логика
боя распределена между Character (умеет атаковать и получать урон)
и Battle (отвечает за проведение раундов и определение победителя).
"""

from typing import List


class Character:
    """Персонаж боя: хранит характеристики и умеет атаковать/получать урон."""

    def __init__(self, name: str, health: int, attack: int, defense: int) -> None:
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack
        self.defense = defense

    def is_alive(self) -> bool:
        """Жив ли персонаж."""
        return self.health > 0

    def calculate_damage_to(self, target: "Character") -> int:
        """Считает урон, который этот персонаж нанесёт цели."""
        return max(1, self.attack_power - target.defense)

    def take_damage(self, damage: int) -> None:
        """Получает урон, здоровье не опускается ниже 0."""
        self.health = max(0, self.health - damage)

    def attack_target(self, target: "Character") -> int:
        """Атакует цель и возвращает нанесённый урон."""
        damage = self.calculate_damage_to(target)
        target.take_damage(damage)
        return damage

    def __str__(self) -> str:
        return f"{self.name} ({self.health}/{self.max_health} HP)"


class Battle:
    """Отвечает за проведение боя между двумя персонажами и ведение лога."""

    def __init__(self, fighter_a: Character, fighter_b: Character) -> None:
        self.fighter_a = fighter_a
        self.fighter_b = fighter_b
        self.log: List[str] = []
        self.winner: Character = None

    def _play_round(self, attacker: Character, defender: Character, round_number: int) -> None:
        damage = attacker.attack_target(defender)
        self.log.append(
            f"Раунд {round_number}: {attacker.name} атакует {defender.name} "
            f"и наносит {damage} урона. У {defender.name} осталось "
            f"{defender.health} HP."
        )

    def simulate(self) -> Character:
        """Проводит бой до победы одного из персонажей и возвращает победителя."""
        round_number = 1
        attacker, defender = self.fighter_a, self.fighter_b

        while self.fighter_a.is_alive() and self.fighter_b.is_alive():
            self._play_round(attacker, defender, round_number)

            if not defender.is_alive():
                break

            attacker, defender = defender, attacker
            round_number += 1

        self.winner = self.fighter_a if self.fighter_a.is_alive() else self.fighter_b
        return self.winner

    def print_result(self) -> None:
        """Выводит лог боя и победителя в консоль."""
        for line in self.log:
            print(line)
        print(f"\nПобедитель: {self.winner.name}!")


def demo() -> None:
    """Демонстрационный сценарий с несколькими примерами боёв."""
    print("=== Бой 1: Воин против Разбойника ===")
    warrior = Character("Воин", health=30, attack=8, defense=4)
    rogue = Character("Разбойник", health=25, attack=9, defense=2)
    battle = Battle(warrior, rogue)
    battle.simulate()
    battle.print_result()

    print("\n=== Бой 2: Маг против Голема ===")
    mage = Character("Маг", health=20, attack=10, defense=1)
    golem = Character("Голем", health=40, attack=5, defense=6)
    battle = Battle(mage, golem)
    battle.simulate()
    battle.print_result()


if __name__ == "__main__":
    demo()
