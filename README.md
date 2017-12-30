# The Game of Life

Conway's Game of Life is a cellular automaton invented in 1970 by the homonymous British mathematician. The aim of the game is to show how natural behaviours like birth, growth and dead of living organisms, who interact with each other in a common environment, can be described with mathematical models and rules.
This game is a zero-player game: the user only has to provide the initial state and this state evolves based on simple rules.

## Rules
The game is played in a board: every tile of the board corresponds to a cell which can be active or inactive, at the initial state. Once the user starts the game, the subsequent states are computed for each cells considering the 8 surrounding neighbours. The rules are:

- Each populated location with one or zero neighbors dies (**loneliness**).
- Each populated location with four or more neighbors dies (**overpopulation**).
- Each populated location with two or three neighbors survives.
- Each unpopulated location becomes populated if it has exactly three populated neighbors (**birth**). 
- All updates are performed simultaneously **in parallel**.

## Implementation
The game has been implemented by using Numpy and Scipy to define the model and to update the state, while PyQT has been used to implement the graphic user interface. The pattern MVC has been used to obtain a separation of concerns between the classes involved in this implementation.

### Model
The model has been implemented in the class `GameOfLifeModel`. This class provides a model that represents the state where the cells live. It also provides methods to get and set information, load, save and clear a state and a method that compute the evolution of the states by convolution (the rules of the game).

### View & Controller
The GUI (it corresponds to the View and Controller of MVC) has been in the class `MainWindow`. This class provides an interface for the user so that to allow him to play the game. 
The GUI uses some custom Widgets. The most important custom widget is the Board that is used to show the model and the evolution of the states. This class is called `GameOfLifeBoard` and takes advantage of sparsity of the model to quickly update the view, from a state to another. 
This class also provides widget to create dialog widgets, used to load and save patterns.

## Functionalities
The GUI appears like: 
<img width="751" alt="schermata 2017-12-27 alle 18 12 24" src="https://user-images.githubusercontent.com/29773493/34387999-a27f78c8-eb31-11e7-8145-ca2253b2a320.png">


This implementation provides some functionalities:
- **Play/Pause & Step by Step**: The user can start playing the game by clicking on the play/pause button. If the user activates the 'Step by Step' mode clicking on the related checkbox, it is possible to see the evolution of the states one step at a time.
- **Load & Save a Pattern**: The user can save own patterns by clicking the save button. Once a pattern has been saved, it is also possible to load it: clicking on the load button, a dialog Widget will be opened and the user can choose between known patterns and own pattern.
- **Clear the Board**: The user can clear all the board by clicking on the clear button.
- **Speed of Computation**: The user can change the speed of the computation of the evolution of the states, by using the speed slider.
- **Real Time Information**: The user can see information about the number of alive cells and the generation reached during the game.
- **Colors**: To keep track of the age of a cell, the game provides different color for each tile:
1. Black: inactive cell.
2. White: active (alive) cell.
3. Lime: new born cell.
4. Green: cell that lives for more than one generation.
5. Silver: cell that is inactive and has dead at least once.

### Simulation
- Activating and disactivating cells, play and pause the game, using "Step by Step" mode, change speed, clear the board.

![gameoflife](https://user-images.githubusercontent.com/29773493/34388681-5cb57690-eb35-11e7-9cca-3c9a45a2b0ad.gif)

- Loading and saving patterns

![gameoflife2](https://user-images.githubusercontent.com/29773493/34388844-6baa2c76-eb36-11e7-9205-c4ed017a1484.gif)

## License
Licensed under the term of [MIT License](http://en.wikipedia.org/wiki/MIT_License). See attached file LICENSE.


