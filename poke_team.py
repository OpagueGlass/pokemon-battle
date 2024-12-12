"""
This module contains PokeTeam and Trainer Class
"""

__author__ = "Jonah Yip Mathivanan"

from pokemon import *
from pokemon_base import TypeEffectiveness
from data_structures.referential_array import ArrayR
from data_structures.bset import BSet
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
import random
from battle_mode import BattleMode


class PokeTeam:
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "experience", "defence", "battle_power", "level"]

    def __init__(self) -> None:
        """
        Initializes a new instance of the PokeTeam class.

        :complexity: Best and worse case O(1).
        """
        self.team = ArrayR(self.TEAM_LIMIT)
        self.team_count = 0
        self.original_team = None

    def choose_manually(self) -> None:
        """
        Lets the user choose up to 6 Pokemon for their team.

        :complexity: Best O(n) if user does not print the list of Pokemon in the POKE_LIST and worst O(n + m*k), if the
        user does print the list of Pokemon. Input, assignment, instantiation of the pokemon, eval and comparisons are
        all O(1) operations. Creating the referential array is O(n). Showing the pokemon names in the POKE_LIST is
        O(m*k), since the loop runs m times, and printing the names is O(k), where m is the number of pokemon in the
        POKE_LIST and k is the number of characters in the name of the pokemon.

        The loop runs n times so the complexity of the loop is O(n). Since O(n) dominates over O(1), and O(n) + O(n)
        + O(m*k) = O(n + m*k), where n is the number of Pokemon chosen for the team.

        Raises:
            Exception: If the number given is not between 1 and 6
            Exception: If the chosen Pokemon is not in POKE_LIST

        """
        number = 0
        while number < 1 or number > self.TEAM_LIMIT:
            try:
                number = int(input("How many Pokemon (up to 6) would you like to choose?\n"))
                if number < 1 or number > self.TEAM_LIMIT:
                    print("Choose a number between 1 and 6")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 6.")
                
        team = ArrayR(number)
        choice = input("Would you like to see the list of Pokemon? (y/n)\n").lower()
        if choice == "y":
            for pokemon in self.POKE_LIST:
                print(pokemon.__name__)
                
        while self.team_count < number:
            name = input("Enter the name of a Pokemon:\n").capitalize()
            try:
                pokemon = eval(name)
                if pokemon != Pokemon and issubclass(pokemon, Pokemon):
                    team[self.team_count] = pokemon()
                    self.team_count += 1
                else:
                    raise NameError
            except NameError:
                print("Pokemon does not exist. Please try again.")

        self.team = team
        self.original_team = self.team

    def choose_randomly(self) -> None:
        """
        Generates a team of 6 randomly chosen Pokemon.

        :complexity: Best and worse O(n). Initialising the referrential array is O(n). The loop runs n times
        and random.choice, instantiating and assigning the Pokemon to the array is O(1) so the complexity of the loop is
        O(n). O(n) + O(n) = O(n), where n is self.TEAM_LIMIT.

        where n is the number of Pokemon chosen for the team.
        """
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon) - 1)
            self.team[i] = all_pokemon[rand_int]()
            self.team_count += 1
        self.original_team = self.team

    def regenerate_team(self, battle_mode: BattleMode, criterion=None) -> None:
        """
        Heals all of the pokemon to their original HP while preserving their level and evolution.
        
        :complexity: For SET or ROTATE, best and worse case O(n)
                     For OPTIMISE, best O(n*log n) if the order attribute is at the end of the ArraySortedList, worse 
                     O(n^2) if the order_attribute is at the start of the ArraySortedList
                     Where n is the number of Pokemon in the original team for all cases.

        Args:
            battle_mode (BattleMode): The battle mode to be used for the team.
            criterion (String, optional): The criterion to sort the team for Optimise mode. Defaults to None.
        """
        self.reset_team()
        
        # Checks the battle mode and structures the team accordingly
        mode_value = battle_mode.value
        if mode_value <= 1:
            self.assemble_team(battle_mode)
        else:
            self.assign_team(criterion)
    
    def reset_team(self):
        """
        Heals the pokemon and resets the team to the original team while preserving their level and evolution.
        
        :complexity: Best and worse case O(n) where n is the number of Pokemon in the original team.
        """
        # Heals each pokemon to their original health
        for pokemon in self.original_team:
            original_pokemon = type(pokemon)()
            original_health = original_pokemon.get_health()
            pokemon.health = original_health
            
        # Resets the team and team count to the original
        self.team = self.original_team
        self.team_count = len(self.original_team)

    def __getitem__(self, index: int) -> type[Pokemon]:
        """
        Returns the pokemon in position index.

        :complexity: If the team is an ArrayR, best and worse case O(1). 
                     If the team is an ArrayStack, best and worse case O(n) where n is the number of Pokemon in the team. 
                     If the team is a CircularQueue, best and worse case O(n) where n is the number of Pokemon in the team.
                     If the team is an ArraySortedList, best and worse case O(1). 
        Args:
            index (int): The index of the Pokemon in the team.

        Raises:
            IndexError: When the index is out of bounds.

        Returns:
            Pokemon: The pokemon at the specified index as a Pokemon type object.
        """
        if index < 0 or index >= len(self):
            raise IndexError("Index out of bounds")
        
        if type(self.team) is ArrayR:
            item = self.team[index]
        elif type(self.team) is ArrayStack:
            stack = ArrayStack(index)
            for _ in range(index):
                stack.push(self.team.pop())
            item = self.team.peek()
            for _ in range(index):
                self.team.push(stack.pop())
        elif type(self.team) is CircularQueue:
            for _ in range(index - 1):
                self.team.append(self.team.serve())
            item = self.team.serve()
            self.team.append(item)
            for _ in range(len(self) - index):
                self.team.append(self.team.serve())
        elif type(self.team) is ArraySortedList:
            item = self.team[index].value
        return item

    def __len__(self) -> int:
        """
        Returns the current length of the team.

        :complexity: Best and worse O(1) since getting the length of the team is a constant time operation.

        Returns:
            int: The current length of the team as an integer.
        """
        return self.team_count

    def __str__(self) -> str:
        """
        Return a string representation of the PokeTeam instance with the current members of the team, with each member
        on a new line based on the order in the team.

        :complexity: If the team is an ArrayR, best and worse case O(n*m^2).
                     If the team is an ArrayStack, best and worse case O(n*m^2).
                     If the team is a CircularQueue, best and worse case O(n*m^2).
                     If the team is an ArraySortedList, best and worse case O(n*m^2).
                     Where n is the number of Pokemon in the team and m is the number of characters in the string 
                     representation of the Pokemon for each case.
        Returns:
            str: The string representation of the PokeTeam instance
        """
        text = ""
        # Checks the structure of the team and adds the Pokemon to the text acccordingly
        if type(self.team) is ArrayR:
            for pokemon in self.team:
                text += str(pokemon) + "\n"
        elif type(self.team) is ArrayStack:
            stack = ArrayStack(len(self))
            for _ in range(len(self)):
                pokemon = self.team.pop()
                text += str(pokemon) + "\n"
                stack.push(pokemon)
            for _ in range(len(self)):
                self.team.push(stack.pop())
        elif type(self.team) is CircularQueue:
            for _ in range(len(self)):
                pokemon = self.team.serve()
                text += str(pokemon) + "\n"
                self.team.append(pokemon)
        elif type(self.team) is ArraySortedList:
            for i in range(len(self)):
                pokemon = self.team[i].value
                text += str(pokemon) + "\n"
        return text

    def get_order_attribute(self, pokemon: type[Pokemon], criterion: str) -> int:
        """
        Returns the order attribute for the Pokemon based on the criterion

        :complexity: Best case O(Comp==) if the criterion is the first element in the CRITERION_LIST. Worse case 
                     O(n*Comp==) if the criterion is at the end of the CRITERION_LIST, where n is the number of elements
                     in the criterion list, and Comp== is the complexity of string comparison.
        
        Args:
            pokemon (Pokemon): The Pokemon to get the order attribute for.
            criterion (str): The criterion for sorting the battle team.

        Raises:
            Exception: When the criterion is not valid

        Returns:
            float: The order attribute for the Pokemon based on the criterion
        """ 
        if criterion not in self.CRITERION_LIST:
            raise Exception("Invalid criterion")
        
        # Gets the order attribute based on the criterion
        index = self.CRITERION_LIST.index(criterion)
        if index == 0:
            order_attribute = pokemon.get_health()
        elif index == 1:
            order_attribute = pokemon.get_experience()
        elif index == 2:
            order_attribute = pokemon.get_defence()
        elif index == 3:
            order_attribute = pokemon.get_battle_power()
        elif index == 4:
            order_attribute = pokemon.get_level()       
        return order_attribute

    def assign_team(self, criterion: str = None) -> None:
        """
        Assigns the order of the team based on the chosen attribute.

        :complexity: Best O(n*log n) if the order attribute is at the end of the ArraySortedList, worse O(n^2) if the 
        order_attribute is at the start of the ArraySortedList, where n is the number of Pokemon in the team.

        Args:
            criterion (str): The chosen attribute for sorting the battle team.
        """
        # Adds each pokemon with their order attribute to the ordered team      
        ordered_team = ArraySortedList(len(self))
        for pokemon in self.team:
            order_attribute = self.get_order_attribute(pokemon, criterion)
            pokemon_item = ListItem(pokemon, order_attribute)
            ordered_team.add(pokemon_item)
        self.team = ordered_team

    def assemble_team(self, battle_mode: BattleMode) -> None:
        """
        Places the pokemon in the appropriate ADT when a battle mode is selected.

        :complexity: For SET and ROTATE, best and worse case O(n+Comp==) where n is the number of Pokemon in the 
                     original team and Comp== is the complexity of integer comparison.

        Args:
            battle_mode (BattleMode): The battle mode
            criterion (str, optional): The chosen attribute for sorting the battle team. Defaults to None.

        Raises:
            Exception: When the battle mode is not valid
        """
        # Assembles the team based on the battle mode
        mode_value = battle_mode.value
        if mode_value == 0:
            team = ArrayStack(len(self))
            for pokemon in self.original_team:
                team.push(pokemon)
        elif mode_value == 1:
            team = CircularQueue(len(self))
            for pokemon in self.original_team:
                team.append(pokemon)
        else:
            raise Exception("Invalid battle mode")
        self.team = team

    def set_special(self):
        """
        Special method for SET mode which reverse the first half of the team.
        
        :complexity: Best and worse case O(n) where n is the number of Pokemon in the team.
        """
        # Gets half the size of the team (rounded down)
        size = len(self.team) // 2
        # Pops the first half of the team and adds it to a queue
        queue = CircularQueue(size)
        for _ in range(size):
            pokemon = self.team.pop()
            queue.append(pokemon)
        # Adds the pokemon back to the team in reversed order
        for _ in range(size):
            pokemon = queue.serve()
            self.team.push(pokemon)

    def rotate_special(self):
        """
        Special method for ROTATE mode which reverse the bottom half of the team.
        
        :complexity: Best and worse case O(n) where n is the number of Pokemon in the team.
        """
        # Gets half the size of the team (rounded down)
        size = len(self.team) // 2
        stack = ArrayStack(size)
        # Skips the first half of the team
        for _ in range(len(self.team) - size):
            pokemon = self.team.serve()
            self.team.append(pokemon)
        # Pushes the bottom half of the team into a stack
        for _ in range(size):
            pokemon = self.team.serve()
            stack.push(pokemon)
        # Adds the pokemon back to the team in reversed order
        for _ in range(size):
            pokemon = stack.pop()
            self.team.append(pokemon)

    def optimise_special(self):
        """
        Special method for OPTIMISE mode which toggles the sorting order (ascending or descending)
        
        :complexity: Best O(n*log n) if the order attribute is at the end of the ArraySortedList, worse O(n^2) if the 
                     order_attribute is at the start of the ArraySortedList, where n is the number of Pokemon in the 
                     team.
        """
        # Changes the order attribute of each pokemon to the negative of the current order attribute
        negative = self.team[0].key < 0
            
        for i in range(len(self.team)):
            index = 0 if negative else i
            item = self.team.delete_at_index(index)
            item.key = -item.key
            self.team.add(item)

    def special(self, battle_mode: BattleMode):
        """
        Shuffles the team based on the battle mode

        :complexity: If the battle mode is SET, best and worse case O(n).
                     If the battle mode is ROTATE, best and worse case O(n).
                     If the battle mode is OPTIMISE, best O(n*log n) if the order attribute is at the end of the 
                     ArraySortedList, worse O(n^2) if the order_attribute is at the start of the ArraySortedList.
                     Where n is the number of Pokemon in the team for each case.
                     
        Args:
            battle_mode (BattleMode): The battle mode
        """
        # Checks the battle mode and calls the appropriate special method
        mode_value = battle_mode.value
        if mode_value == 0:
            self.set_special()
        elif mode_value == 1:
            self.rotate_special()
        elif mode_value == 2:
            self.optimise_special()
    
    def update_optimise_team(self, pokemon: Pokemon, key: float, criterion: str) -> None:
        """
        Updates the optimise team after a round of battle.
        
        :complexity: Best O(log n) if the pokemon is added at the end of the ArraySortedList, worse O(n) if the pokemon 
                     is at the front of the ArraySortedList, where n is the number of Pokemon in the team.

        Args:
            pokemon (Pokemon): The trainer's Pokemon.
            key (float): The order attribute of the Pokemon.
            criterion (str): The criterion for sorting the battle team.
        """
        if pokemon.is_alive():
            order_attribute = self.get_order_attribute(pokemon, criterion)
            if key < 0:
                order_attribute = -order_attribute
            pokemon_item = ListItem(pokemon, order_attribute)
            self.team.add(pokemon_item)


class Trainer:
    def __init__(self, name="Unknown") -> None:
        """
        Initializes a new instance of the Trainer class.
        
        :complexity: Best and worse case O(1).
        """
        self.name = name
        self.poketeam = PokeTeam()
        self.pokedex = BSet(len(TypeEffectiveness()))
        self.lives = 0

    def pick_team(self, method: str) -> None:
        """
        Picks a team based on the mode that is supplied to the method (only "Random" or "Manual" ) as an argument

        :complexity: If the method is "Random", best and worse case O(n+Comp==), where n is the TEAM_LIMIT of Pokemon 
                     that can be in a team and Comp== is the complexity of String comparison.
                     If the method is "Manual", best and worse case O(n+Comp==), where n is the number of Pokemon the
                     user wants to choose and Comp== is the complexity of String comparison.

        Args:
            method (str): The mode to pick the team.

        Raises:
            Exception: If the method is not "Random" or "Manual"
        """
        if method == "Random":
            self.poketeam.choose_randomly()
        elif method == "Manual":
            self.poketeam.choose_manually()
        else:
            raise Exception("Invalid method")

        for pokemon in self.get_team():
            self.register_pokemon(pokemon)

    def get_team(self) -> PokeTeam:
        """
        Returns the PokeTeam of the trainer.
        
        :complexity: Best and worse case O(1).

        Returns:
            PokeTeam: The PokeTeam of the trainer.
        """
        return self.poketeam

    def get_name(self) -> str:
        """
        Returns the name of the trainer.
        
        :complexity: Best and worse case O(1).

        Returns:
            str: The name of the trainer.
        """
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        Registers a Pokemon as seen on the trainer's Pokedex.
        
        :complexity: Best case and worse case O(1).

        Args:
            pokemon (Pokemon): The Pokemon as seen on the trainer's Pokedex.
        """
        pokemon_type = pokemon.get_poketype()
        self.pokedex.add(pokemon_type.value + 1)

    def get_pokedex_completion(self) -> float:
        """
        Returns the rounded float ratio of the number of different types of pokemon seen over the total number of types
        of Pokemon available rounded to 2 decimal places.
        
        :complexity: Best and worse case O(n), where n is the size of the bit vector of the Pokedex.

        Returns:
            float: The Pokedex completion as a float.
        """
        return round(len(self.pokedex) / len(TypeEffectiveness()), 2)

    def __str__(self) -> str:
        """
        Returns a string of the following format: Trainer <trainer_name> Pokedex Completion: <completion>%
        
        :complexity: Best and worse case O(n), where n is the size of the bit vector of the Pokedex.

        Returns:
            str: The Pokedex completion as a string.
        """
        return f"Trainer {self.get_name()} Pokedex Completion: {int(self.get_pokedex_completion()*100)}%"
