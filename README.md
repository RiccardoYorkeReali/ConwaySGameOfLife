# The Game of Life

Conway's Game of Life is a cellular automaton invented in 1970 by the homonymous British mathematician. The aim of the game was to show how natural behaviours like birth, growth and dead of living organisms, who interact with each other in a common environment, can be described with mathematical models and rules.
This game is a zero-player game: the user only has to provide the initial state and this state evolves based on simple rules.

## Rules
The game is played in a board: every tile of the board corresponds to a cell which can be active or inactive, at the initial state. Once the user starts the game, the subsequent states are computed for each cells considering the 8 surrounding neighbours. The rules are:

- Each populated location with one or zero neighbors dies (**loneliness**).
- Each populated location with four or more neighbors dies (**overpopulation**).
- Each populated location with two or three neighbors survives.
- Each unpopulated location becomes populated if it has exactly three populated neighbors (**birth**). 
- All updates are performed simultaneously **in parallel**.

## Implementation
The game has been implemented by using Numpy and Scipy to define the model and to update the state, while PyQT has been used to implement the graphic user interface. The pattern MVC has been used to obtain a separation of concerns between the classes involved in the game.

### Model
The model has been implemented in the class `GameOfLifeModel`. This class provides a model that represents the state in which the whole cells live. It also provides methods to get and set information, load, save and clear a state and a method that compute the evolution of the states by convolution (the rules of the game).

Attributes:
- **cells**: the current state of the Game.
- **aliveCells**: the number of alive cells.
- **generation**: the generation in which current State's cells live.

### Graphic User Interface
