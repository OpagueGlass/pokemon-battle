"""
This module contains an abstract version of the Pokemon class
"""

__author__ = "Jonah Yip Mathivanan"

from abc import ABC
from math import ceil
from poke_type import PokeType, TypeEffectiveness


class Pokemon(ABC):
    """
    Represents a base Pokemon class with properties and methods common to all Pokemon.
    """

    def __init__(self):
        """
        Initializes a new instance of the Pokemon class.
        
        :complexity: Best and worse case O(1)
        """
        self.health = None
        self.level = None
        self.poketype = None
        self.battle_power = None
        self.evolution_line = None
        self.name = None
        self.experience = None
        self.defence = None
        self.speed = None

    def get_name(self) -> str:
        """
        Returns the name of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            str: The name of the Pokemon.
        """
        return self.name

    def get_health(self) -> int:
        """
        Returns the current health of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            int: The current health of the Pokemon.
        """
        return self.health

    def get_level(self) -> int:
        """
        Returns the current level of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            int: The current level of the Pokemon.
        """
        return self.level

    def get_speed(self) -> int:
        """
        Returns the current speed of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            int: The current speed of the Pokemon.
        """
        return self.speed

    def get_experience(self) -> int:
        """
        Returns the current experience of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            int: The current experience of the Pokemon.
        """
        return self.experience

    def get_poketype(self) -> PokeType:
        """
        Returns the type of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            PokeType: The type of the Pokemon.
        """
        return self.poketype

    def get_defence(self) -> int:
        """
        Returns the defence of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            int: The defence of the Pokemon.
        """
        return self.defence

    def get_evolution(self):
        """
        Returns the evolution line of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            list: The evolution of the Pokemon.
        """
        return self.evolution_line

    def get_battle_power(self) -> int:
        """
        Returns the battle power of the Pokemon.
        
        :complexity: Best and worse case O(1)

        Returns:
            int: The battle power of the Pokemon.
        """
        return self.battle_power

    def attack(self, other_pokemon) -> float:
        """
        Calculates and returns the damage that this Pokemon inflicts on the
        other Pokemon during an attack.
        
        :complexity: Best and worse case O(1)

        Args:
            other_pokemon (Pokemon): The Pokemon that this Pokemon is attacking.

        Returns:
            int: The damage that this Pokemon inflicts on the other Pokemon during an attack.
        """
        attack = self.get_battle_power()
        defense = other_pokemon.get_defence()

        if defense < attack / 2:
            damage = attack - defense
        elif defense < attack:
            damage = ceil(attack * 5 / 8 - defense / 4)
        else:
            damage = ceil(attack / 4)

        multiplier = TypeEffectiveness.get_effectiveness(self.get_poketype(), other_pokemon.get_poketype())
        effective_damage = damage * multiplier
        return effective_damage

    def defend(self, damage: int) -> None:
        """
        Reduces the health of the Pokemon by the given amount of damage, after taking
        the Pokemon's defence into account.
        
        :complexity: Best and worse case O(1)

        Args:
            damage (int): The amount of damage to be inflicted on the Pokemon.
        """
        effective_damage = damage / 2 if damage < self.get_defence() else damage
        self.health = self.health - effective_damage

    def level_up(self) -> None:
        """
        Increases the level of the Pokemon by 1, and evolves the Pokemon if it has
          reached the level required for evolution.
          
        :complexity: Best and worse case O(1)
        """
        self.level += 1
        if len(self.evolution_line) > 0 and self.evolution_line.index(self.name) != len(self.evolution_line) - 1:
            self._evolve()

    def _evolve(self) -> None:
        """
        Evolves the Pokemon to the next stage in its evolution line, and updates
          its attributes accordingly.
        
        :complexity: Best and worse case O(1)
        """
        index = self.get_evolution().index(self.get_name()) + 1
        self.name = self.get_evolution()[index]
        self.battle_power *= 1.5
        self.health *= 1.5
        self.speed *= 1.5
        self.defence *= 1.5

    def is_alive(self) -> bool:
        """
        Checks if the Pokemon is still alive (i.e. has positive health).
        
        :complexity: Best and worse case O(1)

        Returns:
            bool: True if the Pokemon is still alive, False otherwise.
        """
        return self.get_health() > 0

    def __str__(self) -> str:
        """
        Return a string representation of the Pokemon instance in the format:
        <name> (Level <level>) with <health> health and <experience> experience
        
        :complexity: Best and worse case O(1)
        
        Returns:
            str: A string representation of the Pokemon instance.
        """
        return f"{self.name} (Level {self.level}) with {self.get_health()} health and {self.get_experience()} experience"
        
