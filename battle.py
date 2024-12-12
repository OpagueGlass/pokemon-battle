"""
This module contains the Battle Class
"""

__author__ = "Jonah Yip Mathivanan"

from math import ceil
from pokemon import Pokemon
from poke_team import Trainer, PokeTeam
from battle_mode import BattleMode


class Battle:
    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion="health") -> None:
        """
        Initializes a new instance of the Battle class.

        :complexity: Best and worse case O(1)

        Args:
            trainer_1 (Trainer): A trainer in the battle
            trainer_2 (Trainer): Another trainer in the battle
            battle_mode (BattleMode): The battle mode
            criterion (str, optional): The criterion to sort the team for Optimise mode. Defaults to "health".
        """
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        """
        Commences the battle between two trainers

        :complexity: If the battle mode is Set, Best case O(n*max(k1,k2)) if each of a trainer's pokemon faints in one
                     round, and worse case O(n*(m+max(k1,k2))) if it takes multiple rounds for pokemon to faint, where n
                     is the number of pokemon in each team, m is the number of rounds played until one of the pokemon
                     wins and k1 and k2 are the size of the bit vector of the Pokedex for trainer 1 and 2.
                     If the battle mode is Rotate, best and worse case O(n*max(k1,k2)), where n is the number of rounds
                     played until one of the teams win and k1 and k2 are the size of the bit vector of the Pokedex for
                     trainer 1 and 2.
                     If the battle mode is Optimise, best and worse case O(n*(m+max(k1,k2))), where n is the number of
                     rounds played until one of the teams win, m is the number of pokemon in each team and k1 and k2 are
                     the size of the bit vector of the Pokedex for trainer 1 and 2.

        Returns:
            Trainer | None: The winning trainer of the battle, None if it is a draw
        """
        # Assigns the battle modes
        mode_value = self.battle_mode.value
        if mode_value == 0:
            winning_team = self.set_battle()
        elif mode_value == 1:
            winning_team = self.rotate_battle()
        elif mode_value == 2:
            winning_team = self.optimise_battle()

        # Gets the winner of the battle
        if winning_team == self.trainer_1.get_team():
            winner = self.trainer_1
        elif winning_team == self.trainer_2.get_team():
            winner = self.trainer_2
        else:
            winner = None
        return winner

    def _create_teams(self) -> None:
        """
        Randomly picks a team for each trainer and assembles the battle team based on the battle mode and criterion

        :complexity: If the battle mode is Set, best and worse case O(n)
                     If the battle mode is Rotate, best and worse case O(n)
                     If the battle mode is Optimise, best O(n*log n) if the order attribute is at the end of the
                     ArraySortedList, worse O(n^2) if the order_attribute is at the start of the ArraySortedList
                     Where n is the TEAM_LIMIT of Pokemon that can be in a team
        """
        mode_value = self.battle_mode.value
        self.trainer_1.pick_team("Random")
        self.trainer_2.pick_team("Random")
        team1 = self.trainer_1.get_team()
        team2 = self.trainer_2.get_team()
        if mode_value <= 1:
            team1.assemble_team(self.battle_mode)
            team2.assemble_team(self.battle_mode)
        else:
            team1.assign_team(self.criterion)
            team2.assign_team(self.criterion)

    def update_pokedexes(self, pokemon_1: Pokemon, pokemon_2: Pokemon):
        """
        Updates the pokedexes of the trainers with the current pokemons

        :complexity: Best and worse case O(1)

        Args:
            pokemon_1 (Pokemon): Trainer 1's current pokemon
            pokemon_2 (Pokemon): Trainer 2's current pokemon
        """
        self.trainer_1.register_pokemon(pokemon_1)
        self.trainer_1.register_pokemon(pokemon_2)
        self.trainer_2.register_pokemon(pokemon_1)
        self.trainer_2.register_pokemon(pokemon_2)

    def battle_attack(self, attacking_pokemon: Pokemon, defending_pokemon: Pokemon, ratio: float) -> None:
        """
        Calculates the attacking damage and defends the defending pokemon

        :complexity: Best and worse case O(1)

        Args:
            attacking_pokemon (Pokemon): The attacking pokemon
            defending_pokemon (Pokemon): The defending pokemon
            ratio (float): The pokedex completion ratio of the attacker over the defender
        """
        attacking_damage = ceil(attacking_pokemon.attack(defending_pokemon) * ratio)
        defending_pokemon.defend(attacking_damage)

    def faster_round(self, pokemon_1: Pokemon, pokemon_2: Pokemon, ratio: float) -> Pokemon | None:
        """
        Plays round where the pokemon_1 of trainer 1 is faster than pokemon_2 of trainer 2

        :complexity: Best and worse case O(1)

        Args:
            pokemon_1 (Pokemon): Trainer 1's current pokemon
            pokemon_2 (Pokemon): Trainer 2's current pokemon
            ratio (float): The pokedex completion ratio of the attacker over the defender

        Returns:
            Pokemon | None: The winning pokemon of the battle round if a pokemon wins, else None
        """
        self.battle_attack(pokemon_1, pokemon_2, ratio)
        if not pokemon_2.is_alive():
            return self.end_round(pokemon_1, pokemon_2)
        self.battle_attack(pokemon_2, pokemon_1, 1 / ratio)
        return self.end_round(pokemon_1, pokemon_2)

    def slower_round(self, pokemon_1: Pokemon, pokemon_2: Pokemon, ratio: float) -> Pokemon | None:
        """
        Plays round where the pokemon_1 of trainer 1 is slower than pokemon_2 of trainer 2

        :complexity: Best and worse case O(1)

        Args:
            pokemon_1 (Pokemon): Trainer 1's current pokemon
            pokemon_2 (Pokemon): Trainer 2's current pokemon
            ratio (float): The pokedex completion ratio of the attacker over the defender

        Returns:
            Pokemon | None: The winning pokemon of the battle round if a pokemon wins, else None
        """
        self.battle_attack(pokemon_2, pokemon_1, 1 / ratio)
        if not pokemon_1.is_alive():
            return self.end_round(pokemon_1, pokemon_2)
        self.battle_attack(pokemon_1, pokemon_2, ratio)
        return self.end_round(pokemon_1, pokemon_2)

    def simultaneous_round(self, pokemon_1: Pokemon, pokemon_2: Pokemon, ratio: float) -> Pokemon | None:
        """
        Plays round where the pokemon_1 of trainer 1 and pokemon_2 of trainer 2 have the same speed

        :complexity: Best and worse case O(1)

        Args:
            pokemon_1 (Pokemon): Trainer 1's current pokemon
            pokemon_2 (Pokemon): Trainer 2's current pokemon
            ratio (float): The pokedex completion ratio of the attacker over the defender

        Returns:
            Pokemon | None: The winning pokemon of the battle round if a pokemon wins, else None
        """
        # If both pokemon have the same speed
        self.battle_attack(pokemon_1, pokemon_2, ratio)
        self.battle_attack(pokemon_2, pokemon_1, 1 / ratio)
        return self.end_round(pokemon_1, pokemon_2)

    def end_round(self, pokemon_1: Pokemon, pokemon_2: Pokemon) -> Pokemon | None:
        """
        Ends the round of battle between two pokemon

        :complexity: Best and worse case O(1)

        Args:
            pokemon_1 (Pokemon): Trainer 1's current pokemon
            pokemon_2 (Pokemon): Trainer 2's current pokemon
            ratio (float): The pokedex completion ratio of the attacker over the defender

        Returns:
            Pokemon | None: The winning pokemon of the battle round if a pokemon wins, else None
        """
        # Checks if both pokemon are alive or fainted
        if not pokemon_1.is_alive() and not pokemon_2.is_alive():
            return None
        elif pokemon_1.is_alive() and pokemon_2.is_alive():
            pokemon_1.health -= 1
            pokemon_2.health -= 1
            if pokemon_1.is_alive() and pokemon_2.is_alive():
                return None

        # Updates the team and pokemon if either one of the pokemon is not alive and declares the winning pokemon
        if not pokemon_1.is_alive():
            self.trainer_1.get_team().team_count -= 1
            pokemon_2.level_up()
            return pokemon_2
        elif not pokemon_2.is_alive():
            self.trainer_2.get_team().team_count -= 1
            pokemon_1.level_up()
            return pokemon_1

    def battle_round(self, pokemon_1: Pokemon, pokemon_2: Pokemon, ratio: float) -> Pokemon | None:
        """
        Plays a round of battle between two pokemon

        :complexity: Best and worse case O(1)

        Args:
            pokemon_1 (Pokemon): Trainer 1's current pokemon
            pokemon_2 (Pokemon): Trainer 2's current pokemon
            ratio (float): The pokedex completion ratio of the attacker over the defender

        Returns:
            Pokemon | None: The winning pokemon of the battle round if a pokemon wins, else None
        """
        # Checks the speed of both pokemon and plays the round accordingly
        if pokemon_1.get_speed() > pokemon_2.get_speed():
            winning_pokemon = self.faster_round(pokemon_1, pokemon_2, ratio)
        elif pokemon_1.get_speed() < pokemon_2.get_speed():
            winning_pokemon = self.slower_round(pokemon_1, pokemon_2, ratio)
        else:
            winning_pokemon = self.simultaneous_round(pokemon_1, pokemon_2, ratio)
        return winning_pokemon

    def battle_rounds(self, pokemon_1: Pokemon, pokemon_2: Pokemon, ratio: float) -> Pokemon | None:
        """
        Plays multiple rounds of battle between two pokemon

        :complexity: Best case O(1) if one of the pokemon wins in one round, and worse case O(n) if it takes multiple
                     rounds, where n is the number of rounds played until one of the pokemon wins.

        Args:
            pokemon_1 (Pokemon): Trainer 1's current pokemon
            pokemon_2 (Pokemon): Trainer 2's current pokemon
            ratio (float): The pokedex completion ratio of the attacker over the defender

        Returns:
            Pokemon | None: The winning pokemon of the battle round if a pokemon wins, else None
        """
        winning_pokemon = None
        while pokemon_1.is_alive() and pokemon_2.is_alive():
            winning_pokemon = self.battle_round(pokemon_1, pokemon_2, ratio)
        return winning_pokemon

    def get_battle_winner(self) -> PokeTeam | None:
        """
        Gets the winning trainer of the battle

        :complexity: Best and worse case O(1)

        Returns:
            PokeTeam | None: The winning PokeTeam of the battle, else None if it is a draw
        """
        team1 = self.trainer_1.get_team().team
        team2 = self.trainer_2.get_team().team
        if team1.is_empty() and team2.is_empty():
            return None
        elif team1.is_empty():
            return self.trainer_2.get_team()
        elif team2.is_empty():
            return self.trainer_1.get_team()

    def set_battle(self) -> PokeTeam | None:
        """
        Plays the battle in Set mode

        :complexity: Best case O(n*max(k1,k2)) if each of a trainer's pokemon faints in one round, and worse case
                     O(n*(m+max(k1,k2))) if it takes multiple rounds for pokemon to faint, where n is the number of
                     pokemon in each team, m is the number of rounds played until one of the pokemon wins and k1 and k2
                     are the size of the bit vector of the Pokedex for trainer 1 and 2.

        Returns:
            PokeTeam | None: The winning PokeTeam of the battle, else None if it is a draw
        """
        team1 = self.trainer_1.get_team().team
        team2 = self.trainer_2.get_team().team
        while not team1.is_empty() and not team2.is_empty():
            pokemon_1 = team1.peek()
            pokemon_2 = team2.peek()
            self.update_pokedexes(pokemon_1, pokemon_2)
            ratio = self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion()
            winning_pokemon = self.battle_rounds(pokemon_1, pokemon_2, ratio)
            if winning_pokemon is pokemon_1:
                team2.pop()
            elif winning_pokemon is pokemon_2:
                team1.pop()
            else:
                team1.pop()
                team2.pop()
        return self.get_battle_winner()

    def rotate_battle(self) -> PokeTeam | None:
        """
        Plays the battle in Rotate mode

        :complexity: Best and worse case O(n*max(k1,k2)), where n is the number of rounds played until one of the teams
                     win and k1 and k2 are the size of the bit vector of the Pokedex for trainer 1 and 2.

        Returns:
            PokeTeam | None: The winning PokeTeam of the battle, else None if it is a draw
        """
        team1 = self.trainer_1.get_team().team
        team2 = self.trainer_2.get_team().team
        while not team1.is_empty() and not team2.is_empty():
            pokemon_1 = team1.serve()
            pokemon_2 = team2.serve()
            self.update_pokedexes(pokemon_1, pokemon_2)
            ratio = self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion()
            self.battle_round(pokemon_1, pokemon_2, ratio)
            if pokemon_1.is_alive():
                team1.append(pokemon_1)
            if pokemon_2.is_alive():
                team2.append(pokemon_2)
        return self.get_battle_winner()

    def optimise_battle(self) -> PokeTeam | None:
        """
        Plays the battle in Optimise mode

        :complexity: Best and worse case O(n*(m+max(k1,k2))), where n is the number of rounds played until one of the
                     teams win, m is the number of pokemon in each team and k1 and k2 are the size of the bit vector of
                     the Pokedex for trainer 1 and 2.

        Returns:
            PokeTeam | None: The winning PokeTeam of the battle, else None if it is a draw
        """
        team1 = self.trainer_1.get_team().team
        team2 = self.trainer_2.get_team().team
        while not team1.is_empty() and not team2.is_empty():
            pokemon_1_item = team1.delete_at_index(0)
            pokemon_2_item = team2.delete_at_index(0)
            pokemon_1_key = pokemon_1_item.key
            pokemon_2_key = pokemon_2_item.key
            pokemon_1 = pokemon_1_item.value
            pokemon_2 = pokemon_2_item.value
            self.update_pokedexes(pokemon_1, pokemon_2)
            ratio = self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion()
            self.battle_round(pokemon_1, pokemon_2, ratio)
            self.trainer_1.get_team().update_optimise_team(pokemon_1, pokemon_1_key, self.criterion)
            self.trainer_2.get_team().update_optimise_team(pokemon_2, pokemon_2_key, self.criterion)
        return self.get_battle_winner()
