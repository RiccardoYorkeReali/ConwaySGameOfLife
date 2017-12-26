# The Game of Life

Conway's Game of Life is a cellular automaton invented in 1970 by the homonymous British mathematician. The aim of the game was to show how natural behaviours like birth, growth and dead of living organisms, who interact with each other in a common environment, can be described with mathematical models and rules.
This game is a zero-player game: the user only has to provide the initial state and this state evolves based on simple rules.

## Rules
The game is played in a board: every tile of the board corresponds to a cell which can be active or inactive, at the initial state. Once the user starts the game, the subsequent states are computed for each cells considering the 8 surrounding neighbours. The rules are:
Attributes:
1. Each populated location with one or zero neighbors dies (from loneliness).
2. Each populated location with four or more neighbors dies (from overpopulation).
3. Each populated location with two or three neighbors survives.
4. Each unpopulated location that becomes populated if it has exactly **three** populated neighbors. 
5. All updates are performed simultaneously **in parallel**.
