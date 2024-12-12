"""
This module contains the CreateExample, BattleExample, and TowerExample classes
"""

__author__ = "Jonah Yip Mathivanan"

import random
from battle import Battle, BattleMode
from poke_team import Trainer
from tower import BattleTower


class CreateExample:
    """
    This class demonstrates the Trainer class and the manual and random team selection.
    """

    def run_example(self) -> None:
        name = input("Enter your the name of the trainer:\n")
        trainer = Trainer(name)
        response = input(f"Welcome {trainer.get_name()}! Would you like to manually pick your team (y/n)?\n").lower()
        if response == "y":
            trainer.pick_team("Manual")
        elif response == "n":
            trainer.pick_team("Random")
        else:
            print("Invalid response. Defaulting to random selection.")
            trainer.pick_team("Random")
        print("--------------------------------------------")
        print(f"{trainer.get_name()}'s team")
        print("--------------------------------------------")
        print(trainer.get_team())
        print(trainer)


class BattleExample:
    """
    This class demonstrates the Battle class with different battle modes and their special methods.
    
    Default seed can be changed to test with different teams.
    """

    DEFAULT_SEED = 20

    def __init__(self) -> None:
        self.trainer1 = Trainer("Gary")
        self.trainer2 = Trainer("Ash")

    def __create_battle(self, battle_mode: BattleMode, criterion: str = "health") -> Battle:
        random.seed(self.DEFAULT_SEED)
        battle = Battle(self.trainer1, self.trainer2, battle_mode, criterion=criterion)
        battle._create_teams()
        return battle

    def __reset_trainers(self) -> None:
        self.trainer1.pokedex.clear()
        self.trainer2.pokedex.clear()
        self.trainer1.get_team().reset_team()
        self.trainer2.get_team().reset_team()

    def __start_message(self, battle_mode: BattleMode) -> None:
        print("--------------------------------------------")
        print(f"Starting {battle_mode.name} battle")
        print("--------------------------------------------")

    def __display_team(self, trainer: Trainer) -> None:
        print(f"{trainer.get_name()}'s Team:")
        if len(trainer.get_team()) > 0:
            print(trainer.get_team())
        else:
            print(f"{trainer.get_name()} has no Pokemon left in their team.\n")

    def __summary(self, trainer: Trainer) -> None:
        self.__display_team(trainer)
        print(trainer)

    def __end_battle(self, winner: Trainer) -> None:
        print("Winner:", winner.get_name(), "\n")
        self.__summary(self.trainer1)
        print("----------------------")
        self.__summary(self.trainer2)
        self.__reset_trainers()

    def __set_battle(self) -> None:
        self.__start_message(BattleMode.SET)
        battle = self.__create_battle(BattleMode.SET)
        self.trainer1.get_team().special(BattleMode.SET)
        winner = battle.commence_battle()
        self.__end_battle(winner)

    def __rotate_battle(self) -> None:
        self.__start_message(BattleMode.ROTATE)
        battle = self.__create_battle(BattleMode.ROTATE)
        winner = battle.commence_battle()
        self.__end_battle(winner)

    def __optimise_battle(self) -> None:
        self.__start_message(BattleMode.OPTIMISE)
        battle = self.__create_battle(BattleMode.OPTIMISE, "health")
        winner = battle.commence_battle()
        self.__end_battle(winner)

    def run_example(self) -> None:
        self.__set_battle()
        self.__rotate_battle()
        self.__optimise_battle()


class TowerExample:
    """
    This class demonstrates the BattleTower class.

    Default seed can be changed to test with different teams for the player and enemies, and the default battle mode can
    be changed to test with different battle modes.
    """

    DEFAULT_SEED = 200
    DEFAULT_BATTLE_MODE = BattleMode.ROTATE

    def __init__(self) -> None:
        random.seed(self.DEFAULT_SEED)
        self.player_trainer = Trainer("Ash")
        self.player_trainer.pick_team("Random")
        self.player_trainer.get_team().assemble_team(self.DEFAULT_BATTLE_MODE)

        self.bt = BattleTower()
        self.bt.MIN_LIVES = 2
        self.bt.MAX_LIVES = 10
        self.bt.set_my_trainer(self.player_trainer)
        self.bt.generate_enemy_trainers(2)

    def run_example(self):
        print("--------------------------------------------")
        print("Starting Battle Tower")
        print("--------------------------------------------")
        while self.bt.battles_remaining():
            self.bt.next_battle()
        print("Number of enemies defeated:", self.bt.enemies_defeated())
        print(f"{self.player_trainer.get_name()}'s team:")
        print(self.player_trainer.get_team())
        print(self.player_trainer)


def start_game():
    response = input("Run Create, Battle or Tower example? (c/b/t): ").lower()
    if response == "c":
        select = CreateExample()
        select.run_example()
    elif response == "b":
        battle = BattleExample()
        battle.run_example()
    elif response == "t":
        tower = TowerExample()
        tower.run_example()
    else:
        print("Invalid response. Please try again.")


if __name__ == "__main__":
    start_game()
