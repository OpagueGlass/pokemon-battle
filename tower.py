"""
Unless stated otherwise, all methods in this classes are O(1) best/worst case.
This module contains the BattleTower class
"""

__author__ = "Jonah Yip Mathivanan"

import random
from poke_team import Trainer
from data_structures.queue_adt import CircularQueue
from typing import Tuple
from battle_mode import BattleMode
from battle import Battle


class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3

    def __init__(self) -> None:
        """
        Initializes a new instance of the BattleTower class.
        
        :complexity: Best and worst case is O(1)
        """
        self.trainer = None
        self.enemies = None
        self.enemy_lives = 0
        self.defeated_enemies = 0

    def set_my_trainer(self, trainer: Trainer) -> None:
        """
        Sets the trainer for the battle tower, and generates between MIN_LIVES and MAX_LIVES lives

        :complexity: Best and worst case is O(1 * randint)
        
        Args:
            trainer (Trainer): The trainer to set for the battle tower.
        """
        self.trainer = trainer
        lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
        self.trainer.lives = lives

    def generate_enemy_trainers(self, num_teams:int) -> None:
        """
        Generates enemy trainers for the battle tower and generate each team a number of lives between MIN_LIVES and 
        MAX_LIVES
        
        :complexity: Best and worst case is O(n*(m+randint+Comp==)), where n is the number of enemy trainers to 
                     generate, m is the number of Pokemon in each team, and Comp== is the complexity of String 
                     comparison

        Args:
            num_teams (int): The number of enemy trainers to generate.
        """
        self.enemies = CircularQueue(num_teams)
        for _ in range(num_teams):
            enemy = Trainer()
            enemy.pick_team("Random")
            enemy.get_team().assemble_team(BattleMode.ROTATE)
            lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
            enemy.lives = lives
            self.enemy_lives += lives
            self.enemies.append(enemy)

    def battles_remaining(self) -> bool:
        """
        Returns True if there are more battles to be had, False if either the player or all enemy teams have ran out of 
        lives
        
        :complexity: Best and worst case is O(Comp>), where Comp> is the complexity of integer comparison.

        Returns:
            bool: If there are battles remaining in the battle tower.
        """
        return self.enemy_lives > 0 and self.trainer.lives > 0

    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        Simulates one battle in the tower, between the player team and the next enemy team. 
        
        :complexity: Best and worse case O(n*max(k1,k2) + r), where n is the number of rounds played until one of the 
                     teams win, k1 and k2 are the size of the bit vector of the Pokedex for trainer 1 and 2 and r is the
                     complexity of the regenerate_team method in the PokeTeam class, which is affected by the number of
                     Pokemon in the team and the battle mode.

        Returns:
            Tuple[Trainer, Trainer, Trainer, int, int]: The battle result, the player trainer, the enemy trainer, 
            the player lives remaining after the battle, and the enemy lives remaining after the battle
        """
        enemy = self.enemies.serve()
        self.trainer.get_team().regenerate_team(BattleMode.ROTATE)
        enemy.get_team().regenerate_team(BattleMode.ROTATE)
        battle = Battle(self.trainer, enemy, BattleMode.ROTATE)
        winner = battle.commence_battle()
        if winner is self.trainer:
            enemy.lives -= 1
            self.enemy_lives -= 1
            self.defeated_enemies += 1
        elif winner is enemy:
            self.trainer.lives -= 1
        elif winner is None:
            self.trainer.lives -= 1
            enemy.lives -= 1
        if enemy.lives > 0:
            self.enemies.append(enemy)
        return winner, self.trainer, enemy, self.trainer.lives, self.enemy_lives

    def enemies_defeated(self) -> int:
        """Returns the number of enemy lives taken by the player
        
        :complexity: Best and worst case is O(1)

        Returns:
            int: The number of enemy lives taken by the player
        """
        return self.defeated_enemies
