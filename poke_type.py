"""
This module contains the PokeType enum and TypeEffectiveness class
"""

__author__ = "Jonah Yip Mathivanan"

from enum import Enum
from data_structures.referential_array import ArrayR


class PokeType(Enum):
    """
    This enum contains all the different types that a Pokemon could belong to
    """

    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14


class TypeEffectiveness:
    """
    Represents the type effectiveness of one Pokemon type against another.
    """

    def get_effect_table(path) -> ArrayR[ArrayR[float]]:
        """
        Returns a table with the type effectiveness of one Pokemon type against another, where the rows represent the
        attacking type and the columns represent the defending type.
        
        :complexity: Best and worse case O(n^2), where n is the number of types of Pokemon

        Returns:
            ArrayR[ArrayR[float]]: A nested referential array of floats representing the type effectiveness table.
        """
        with open(path) as file:
            size = len(file.readline().split(","))
            table = ArrayR(size)

            for row_index, line in enumerate(file):
                row = ArrayR(size)
                for value_index, value in enumerate(line.split(",")):
                    row[value_index] = float(value)
                table[row_index] = row
            return table

    DEFAULT_PATH = "type_effectiveness.csv"

    EFFECT_TABLE = get_effect_table(DEFAULT_PATH)

    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        """
        Returns the effectiveness of one Pokemon type against another, as a float.
        
        :complexity: Best and worse case O(1)

        Parameters:
            attack_type (PokeType): The type of the attacking Pokemon.
            defend_type (PokeType): The type of the defending Pokemon.

        Returns:
            float: The effectiveness of the attack, as a float value between 0 and 4.
        """
        return cls.EFFECT_TABLE[attack_type.value][defend_type.value]

    def __len__(self) -> int:
        """
        Returns the number of types of Pokemon
        
        :complexity: Best and worse case O(1)
        
        Returns:
            int: The number of types of Pokemon
        """
        return len(self.EFFECT_TABLE)
