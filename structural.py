"""
Задача 28. Простая ролевая боевая система — СТРУКТУРНЫЙ СТИЛЬ

Данные персонажа хранятся в словаре, вся логика вынесена в отдельные
функции. Функции получают данные как аргументы и возвращают/изменяют их,
но сами по себе не являются частью "объекта" — состояние и поведение
разделены, как того требует структурный подход.
"""

from typing import Dict, List


def create_character(name: str, health: int, attack: int, defense: int) -> Dict:
    """Создаёт словарь-персонажа с базовыми характеристиками."""
    return {
        "name": name,
        "health": health,
        "max_health": health,
        "attack": attack,
        "defense": defense,
    }


def is_alive(character: Dict) -> bool:
    """Проверяет, жив ли персонаж (health > 0)."""
    return character["health"] > 0


def calculate_damage(attacker: Dict, defender: Dict) -> int:
    """Считает урон: max(1, атака атакующего - защита защищающегося)."""
    return max(1, attacker["attack"] - defender["defense"])


def apply_damage(character: Dict, damage: int) -> None:
    """Уменьшает здоровье персонажа на величину урона (не ниже 0)."""
    character["health"] = max(0, character["health"] - damage)


def take_turn(attacker: Dict, defender: Dict, round_number: int, log: List[str]) -> None:
    """Один ход: атакующий бьёт защищающегося, результат пишется в лог."""
    damage = calculate_damage(attacker, defender)
    apply_damage(defender, damage)
    log.append(
        f"Раунд {round_number}: {attacker['name']} атакует {defender['name']} "
        f"и наносит {damage} урона. У {defender['name']} осталось "
        f"{defender['health']} HP."
    )


def simulate_battle(fighter_a: Dict, fighter_b: Dict) -> Dict:
    """
    Симулирует бой до тех пор, пока один из персонажей не будет повержен.

    Возвращает словарь с логом раундов и именем победителя.
    """
    log: List[str] = []
    round_number = 1

    # Персонажи ходят по очереди, начинает fighter_a
    attacker, defender = fighter_a, fighter_b

    while is_alive(fighter_a) and is_alive(fighter_b):
        take_turn(attacker, defender, round_number, log)

        if not is_alive(defender):
            break

        attacker, defender = defender, attacker
        round_number += 1

    winner = fighter_a if is_alive(fighter_a) else fighter_b

    return {"log": log, "winner": winner["name"]}


def print_battle_result(result: Dict) -> None:
    """Выводит лог боя и победителя в консоль."""
    for line in result["log"]:
        print(line)
    print(f"\nПобедитель: {result['winner']}!")


def demo() -> None:
    """Демонстрационный сценарий с несколькими примерами боёв."""
    print("=== Бой 1: Воин против Разбойника ===")
    warrior = create_character("Воин", health=30, attack=8, defense=4)
    rogue = create_character("Разбойник", health=25, attack=9, defense=2)
    result = simulate_battle(warrior, rogue)
    print_battle_result(result)

    print("\n=== Бой 2: Маг против Голема ===")
    mage = create_character("Маг", health=20, attack=10, defense=1)
    golem = create_character("Голем", health=40, attack=5, defense=6)
    result = simulate_battle(mage, golem)
    print_battle_result(result)


if __name__ == "__main__":
    demo()
