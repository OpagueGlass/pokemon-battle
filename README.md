# Pokemon Battle

## Overview

Building a game using efficient algorithms with optimal basic data structures, while evaluating their performance by
analysing the best and worst-case Big-O time complexities.

## Introduction

Welcome to the exciting world of Pokemon! Pokemon Battles is a game where teams of opposing Pokémon fight to determine
the winner. The pokemon monsters are the cornerstone of the battles, each with unique types, stats, and evolution lines.
With 77 pokemon to manually or randomly choose from, the variety makes the game engaging and dynamic.

## Pokemon Attributes

- **Health**: Indicates the health points a Pokemon has before fainting, which reduces when the pokemon is attacked.
- **Level**: Increases by 1 when a Pokemon defeats the opposing pokemon, boosting their defence, battle power, health
and defence.
- **Defence**: Represents the resistance from attacks.
- **Type**: Affects the damage inflicted to other Pokemon.
- **Battle Power**: Indicates the base damage dealt during battles.
- **Name**: The name of the Pokemon.
- **Evolution Line**: Lists the evolution stages of the Pokemon.
- **Experience**: Gained from battling other pokemon
- **Speed**: Determines the attack order in battles, with faster Pokemon attacking before slower ones.

## Battling

Battles between two teams are turn-based, with each team selecting one Pokemon to fight while the rest wait. Turns
continue until one or both teams have no Pokemon remaining. If a Pokémon faints, a new one from the team is sent out at
the end of the turn.

Each team can either select the **Attack** or **Special** action every turn

- **Attack**: The active Pokémon attacks the opponent's active Pokémon.
- **Special**: The active Pokémon is swapped out, and the team's special method is called.

### Battle Modes

There are three battle modes in which battles can be fought.

1. **Set Mode**: Follows the 'King of the Hill' style of combat where a Pokemon keeps fighting until it faints, gaining
   experience and leveling up if it defeats an opponent.
2. **Rotating Mode**: Pokemon are sent to the back of the team after each round, with the next in line fighting the next
   round.
3. **Optimised Mode**: Teams are ordered by a chosen attribute (Level, HP, Attack, Defense, Speed), with the order
   maintained throughout the battle even when the stats change each round.

### Special Method

When the **Special** action is selected, the following occurs based on the battle mode:

- **Set Mode**: Reverses the first half of the team.
- **Rotating Mode**: Reverses the bottom half of the team.
- **Optimised Mode**: Toggles the sorting order.

## Battle Tower

The player faces a series of enemy teams with a battle mode. Both the player's and enemy teams has a set number of lives. The enemy teams take it in turns to battle the player's team, and the result is either a win/loss or draw. The
losing team loses a life, and in the result of a draw both teams lose a life.

The order in which enemy teams face the player team is determined as follows:

1. An initial order for the enemy teams is established.
2. After all enemy teams have battled the player team, those with at least one life remaining will fight the player
   again, following the same initial order.
3. Before each battle, `regenerate_team` is called on both teams to heal and revive all Pokémon.

For example, if there are 3 enemy trainers, X, Y, and Z, with 2, 1, and 3 lives respectively, and the player wins every
battle:

1. The player faces trainers X, Y, and then Z.
2. The player faces trainers X and then Z.
3. The player faces trainer Z.

Battles continue until either the player or all enemy teams have no lives left.

## Instructions

1. Clone the repository
2. Run the example script `example.py`
3. Select a feature to demonstrate and proceed with the console instructions
4. Change the default seed in the example classes and rerun the battle with different team compositions
