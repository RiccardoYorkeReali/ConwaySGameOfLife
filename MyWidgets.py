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

import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QLabel, QWidget, QVBoxLayout, QHBoxLayout, 
                            QGroupBox, QListWidget, QTextEdit, QListWidgetItem, QDialog)

### MY WIDGETS

class PlayPauseStepButton(QPushButton):
    """ Custom Button used to play and pause the Game. If Step-by-Step mode is activated, this button let the user proceed step by step 
        
        Attributes:
            status    represent the current mode of the button.
    """
    
    def __init__(self):
        """ Init Method """
        super().__init__()

        self.setFixedWidth(100)

        self.status = "Pause"
        self.setText("Play")
        self.clicked.connect(self.updatePPSButton)

    def updatePPSButton(self):
        """ Method that toggles the text, based on the 'status' attribute """
        if self.getStatus() != "Step by Step":
            if self.getStatus() == "Pause":
                self.setText("Pause")
                self.setStatus("Play")
            else:
                self.setText("Play")
                self.setStatus("Pause")
        else:
            self.setText("Next Step")
            self.setStatus("Step by Step")

    def setStatus(self, status):
        """ Method to set the status of the Button """
        self.status = status

    def getStatus(self):
        """ method to get the status of the Button """
        return self.status


class infoLabel(QLabel):
    """ Custom Label used to display information about the number of alive cells and the current generation

        Attribute:
            informationTarget   represents the displayed information (required)
            informationValue    represents the value of the displayed information
    """

    def __init__(self, informationTarget):
        """ Init Method """
        super().__init__()

        self.informationTarget = informationTarget
        self.informationValue = 0
        self.setText(self.informationTarget + str(self.informationValue))

    def updateInfoLabel(self, informationValue):
        """ Method to update the displayed information """
        self.informationValue = informationValue
        self.setText(self.informationTarget + str(self.informationValue))

class loadWindow(QDialog):
    """ Custom Widget used to let the user load a Pattern. The user can choose between known Patterns and own Patterns 
        Attribute:
            model       reference to the model
            board       reference to the Widget that displays the model information
            aliveCells  reference to the Label that shows the number of alive cells
            generation  reference to the label that shows the current generation
            mainWindow  reference to the main Window 
        """
    def __init__(self, model, board, cells, generation, mainWindow):
        """ Init Mehod """
        super().__init__()
        
        self.model = model
        self.board = board
        self.aliveCells = cells
        self.generation = generation
        self.mainWindow = mainWindow

        self.setModal(True)

        self.setMinimumSize(500, 500)
        self.setMaximumSize(500, 500) 

        # the path needed to load the patterns
        knownPath = 'knownPatterns/'
        myPath = 'myPatterns/'
        
        # creating layout..
        knownPatternBox = QGroupBox('Known Patterns')
        knownPatternLayout = QVBoxLayout()
        self.knownPatternList = QListWidget()
        self.loadButton1 = QPushButton('Load')
        self.loadButton1.setFixedWidth(70)

        # checking if directory of known patterns exist and extracting them
        knownDirectory = os.path.dirname(knownPath)
        if  os.path.exists(knownDirectory):
            files = os.listdir(knownDirectory)
            for f in files:
                itm = QListWidgetItem(f)
                self.knownPatternList.addItem(itm)
            self.loadButton1.clicked.connect(self.loadKnownPattern)
            self.knownPatternList.setCurrentItem(self.knownPatternList.item(0))

        # creating layout..
        loadBoxLayout = QHBoxLayout()
        loadBoxLayout.addStretch()
        loadBoxLayout.addStretch()
        loadBoxLayout.addWidget(self.loadButton1)
        loadWidget = QWidget()
        loadWidget.setLayout(loadBoxLayout)
        knownPatternLayout.addWidget(self.knownPatternList)
        knownPatternLayout.addWidget(loadWidget)

        knownPatternBox.setLayout(knownPatternLayout)

        myPatternBox = QGroupBox('My Patterns')
        myPatternLayout = QVBoxLayout()
        self.myPatternList = QListWidget()
        self.loadButton2 = QPushButton('Load')
        self.loadButton2.setFixedWidth(70)

        # checking if directory of own patterns exist and extracting them
        myDirectory = os.path.dirname(myPath)
        if  os.path.exists(myDirectory):
            files = os.listdir(myDirectory)
            for f in files:
                itm = QListWidgetItem(f)
                self.myPatternList.addItem(itm)
            self.loadButton2.clicked.connect(self.loadMyPattern)
            self.myPatternList.setCurrentItem(self.myPatternList.item(0))
        
        # creating layout..

        loadBoxLayout = QHBoxLayout()
        loadBoxLayout.addStretch()
        loadBoxLayout.addStretch()
        loadBoxLayout.addWidget(self.loadButton2)
        loadWidget = QWidget()
        loadWidget.setLayout(loadBoxLayout)
        myPatternLayout.addWidget(self.myPatternList)
        myPatternLayout.addWidget(loadWidget)

        myPatternBox.setLayout(myPatternLayout)

        theLayout = QVBoxLayout()
        theLayout.addWidget(knownPatternBox)
        theLayout.addWidget(myPatternBox)

        self.setLayout(theLayout)
        self.setWindowTitle("Load Pattern")
        
    def loadKnownPattern(self):
        """ Method to load a known pattern """
        path = 'knownPatterns/'
        pattern = self.knownPatternList.currentItem().text()
        
        currentState = self.model.getCurrentState()
        emptyState = self.model.clearModel()
        newState = self.model.loadModel(path, pattern)
        
        self.board.updateView(emptyState, currentState, 'clear')
        self.board.updateView(newState, emptyState, 'load')

        self.aliveCells.updateInfoLabel(self.model.getAliveCells())
        self.generation.updateInfoLabel(self.model.getGeneration())

        self.close()


    def loadMyPattern(self):
        """ Method to load an own pattern """
        path = 'myPatterns/'
        pattern = self.myPatternList.currentItem().text()
        
        currentState = self.model.getCurrentState()
        emptyState = self.model.clearModel()
        newState = self.model.loadModel(path, pattern)
        
        self.board.updateView(emptyState, currentState, 'clear')
        self.board.updateView(newState, emptyState, 'load')

        self.aliveCells.updateInfoLabel(self.model.getAliveCells())
        self.generation.updateInfoLabel(self.model.getGeneration())

        self.close()

class saveWindow(QDialog):
    """ Custom Widget used to let the user save an own Pattern. The user can choose between known Patterns and own Patterns 
        Attribute:
            model       reference to the model
            mainWindow  reference to the main Window 
        """
    def __init__(self, model, mainWindow):
        """ Init Method """
        super().__init__()

        self.model = model
        self.mainWindow = mainWindow

        self.setModal(True)

        self.setMinimumSize(500, 200)
        self.setMaximumSize(500, 200) 

        # creating layout..
        titleBoxLayout = QHBoxLayout()
        titleText = QLabel('Save as: ')
        self.titleInput = QTextEdit('My Pattern')

        titleBoxLayout.addWidget(titleText)
        titleBoxLayout.addWidget(self.titleInput)

        titleWidget = QWidget()
        titleWidget.setLayout(titleBoxLayout)

        saveBoxLayout = QHBoxLayout()
        self.saveButton = QPushButton('Save')
        self.saveButton.setFixedWidth(70)

        saveBoxLayout.addStretch()
        saveBoxLayout.addStretch()
        saveBoxLayout.addWidget(self.saveButton)

        saveWidget = QWidget()
        saveWidget.setLayout(saveBoxLayout)

        theLayout = QVBoxLayout()
        theLayout.addWidget(titleWidget)
        theLayout.addWidget(saveWidget)

        self.setLayout(theLayout)

        self.setWindowTitle("Save Your Pattern")

        self.saveButton.clicked.connect(self.savePattern)

    def savePattern(self):
        """ Method to save on own pattern """
        myTitle = self.titleInput.toPlainText()
        self.model.saveModel(myTitle)
        self.close()
        