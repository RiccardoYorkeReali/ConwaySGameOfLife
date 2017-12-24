##
## MIT License
## 
## Copyright (c) 2017 Riccardo Reali 
## 
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
##

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QSlider, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QGroupBox)
from GameOfLifeBoard import GameOfLifeBoard
from MyWidgets import PlayPauseStepButton, infoLabel, loadWindow, saveWindow

### THE GUI

class MainWindow(QWidget):
    """ Class that implements the main window 
        
        Attributes:
            model     reference to the model
    """
    def __init__(self, model):
        """ Init Method """
        super().__init__()

        self.model = model
        self.init_ui()

    def init_ui(self):
        """ Method to initialize the user interface """

        #CREATING WIDGETS

        #Title
        self.setWindowTitle("The Game of Life")

        #Buttons
        self.clearButton = QPushButton()
        self.clearButton.setText("Clear")
        self.playPauseStepButton = PlayPauseStepButton()
        self.saveButton = QPushButton()
        self.saveButton.setText("Save")
        self.loadButton = QPushButton()
        self.loadButton.setText("Load")

        #Frame-Rate Slider
        self.frameRateSlider = QSlider(Qt.Horizontal)
        self.frameRateSlider.setMinimum(1)
        self.frameRateSlider.setMaximum(500)
        self.frameRateSlider.setValue(250)
        self.frameRateSlider.setTickInterval(10)
        self.frameRateSlider.setTickPosition(QSlider.TicksBelow)

        #Labels
        self.generationLabel = infoLabel('Current Generation: ')
        self.aliveCellsLabel = infoLabel('Alive Cells: ')

        #Modality 
        self.stepByStepMod = QCheckBox("Step by Step")

        #Display
        self.display = GameOfLifeBoard(self.model, self.aliveCellsLabel)
        displayWidget = QWidget()
        displayWidget.setLayout(self.display)

        #Timer
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000 - self.frameRateSlider.value()*2)

        #CREATING LAYOUT...

        #Information Box
        informationBoxLayout = QHBoxLayout()
        informationBoxLayout.addWidget(self.generationLabel)
        informationBoxLayout.addStretch()
        informationBoxLayout.addWidget(self.aliveCellsLabel)

        informationBox = QGroupBox('Information')
        informationBox.setLayout(informationBoxLayout)

        #Command Box
        commandBoxLayout = QHBoxLayout()
        commandBoxLayout.addWidget(QLabel('Speed: '))
        commandBoxLayout.addWidget(self.frameRateSlider)
        commandBoxLayout.addStretch()
        playPauseLayout = QVBoxLayout()
        playPauseLayout.addWidget(self.playPauseStepButton)
        playPauseLayout.addWidget(self.stepByStepMod)
        commandBoxLayout.addLayout(playPauseLayout)
        commandBoxLayout.addStretch()
        commandBoxLayout.addWidget(self.clearButton)
        commandBoxLayout.addWidget(self.saveButton)
        commandBoxLayout.addWidget(self.loadButton)
        commandBoxLayout.setAlignment(Qt.AlignCenter)

        commandBox = QGroupBox('Commands')
        commandBox.setLayout(commandBoxLayout)

        #Main Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(informationBox)
        mainLayout.addWidget(displayWidget)
        mainLayout.addWidget(commandBox)

        self.setLayout(mainLayout)
        self.setMinimumSize(750, 600)
        self.setMaximumSize(750, 600) 

        #Connecting widgets
        self.clearButton.clicked.connect(self.clear)

        self.stepByStepMod.stateChanged.connect(self.toggleStepByStep)
        self.playPauseStepButton.clicked.connect(self.nextStep)
        self.timer.timeout.connect(self.nextStep)
        self.frameRateSlider.valueChanged.connect(self.setSpeed)
        self.loadButton.clicked.connect(self.loadPattern)
        self.saveButton.clicked.connect(self.savePattern)

        self.show()

    def clear(self):
        """ Method which manages the routine that clear the board """
        if self.playPauseStepButton.getStatus() == "Play":
            self.playPauseStepButton.updatePPSButton()

        currentState = self.model.getCurrentState()
        newState = self.model.clearModel()
        self.display.updateView(currentState,newState, 'clear')

        aliveCells = self.model.getAliveCells()
        self.aliveCellsLabel.updateInfoLabel(aliveCells)

        generation = self.model.getGeneration()
        self.generationLabel.updateInfoLabel(generation)

    def toggleStepByStep(self, activate):
        """ Method to enable and disable the step by step mode """
        if activate == Qt.Checked:
            self.playPauseStepButton.setStatus("Step by Step")
            self.playPauseStepButton.updatePPSButton()
        else:
            self.playPauseStepButton.setStatus("Play")
            self.playPauseStepButton.updatePPSButton()

    def nextStep(self):
        """ Method to menages the loop of the game """
        if self.playPauseStepButton.getStatus() == "Step by Step":
            currentState = self.model.getCurrentState()
            newState =  self.model.nextState()
            self.display.updateView(currentState, newState, 'nextStep')

            aliveCells = self.model.getAliveCells()
            self.aliveCellsLabel.updateInfoLabel(aliveCells)

            generation = self.model.getGeneration()
            self.generationLabel.updateInfoLabel(generation)

        else: 
            if self.playPauseStepButton.getStatus() == "Play":
                currentState = self.model.getCurrentState()
                newState =  self.model.nextState()
                self.display.updateView(currentState, newState, 'nextStep')

                aliveCells = self.model.getAliveCells()
                self.aliveCellsLabel.updateInfoLabel(aliveCells)

                generation = self.model.getGeneration()
                self.generationLabel.updateInfoLabel(generation)

                self.timer.start()

    def setSpeed(self):
        """ Method to change the speed of the loop game """
        self.timer.setInterval(1000 - self.frameRateSlider.value()*2)

    def loadPattern(self):
        """ Method to load a pattern """
        self.load = loadWindow(self.model, self.display, self.aliveCellsLabel, self.generationLabel, self)
        self.load.show()

    def savePattern(self):
        """ Method to save a pattern """
        self.save = saveWindow(self.model, self)
        self.save.show()
