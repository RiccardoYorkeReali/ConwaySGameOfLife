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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QStyleOption, QStyle, QWidget)
from PyQt5.QtGui import QPainter

import numpy as np

class GameOfLifeTile(QWidget):
	""" Custom widget that represents a cell of the game.

		Attributes:
			color       the color of the cell (black: inactive, white: active/alive, green: alive for more than a generation, lime: new born, silver: dead)
			deadOnce    boolean value which is set to True if a cell has dead once
			i,j         indices of the cell in the board
			model       reference to the model
			notBlack    reference to the list used to keep track of the tiles that are not black
			aliveCells  reference to the label that display the number of alive cells.
	"""

	def __init__(self, i, j, model, notBlackList, aliveCellsLabel):
		""" Init Method """
		super().__init__()

		self.setFixedWidth(10)
		self.setFixedHeight(10)
		self.setStyleSheet("background: black")
		self.color = "black"
		self.deadOnce = False
		self.i = i 
		self.j = j
		self.model = model
		self.notBlack = notBlackList
		self.aliveCells = aliveCellsLabel

	def paintEvent(self, event):
		""" re-implementation of paintEvent to show subclass of QWidget """
		o = QStyleOption()
		o.initFrom(self)
		p = QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget, o, p, self) 

	def mousePressEvent(self, event):
		""" Method to change the color of a cell. If a cell is pressed, by the reference to the model, the related cell in the model is set as active or inactive """
		if self.color == "black" or self.color == "silver":

			self.setStyleSheet("background: white")
			self.color = "white"
			self.model.setCellActive(self.i , self.j )
			self.notBlack[self.i, self.j] = 1

			self.aliveCells.updateInfoLabel(self.model.getAliveCells())

		elif self.color == "white" and self.deadOnce == False:

			self.setStyleSheet("background: black")
			self.color = "black" 
			self.model.setCellInactive(self.i , self.j )
			self.notBlack[self.i, self.j] = 0

			self.aliveCells.updateInfoLabel(self.model.getAliveCells())

		elif self.color == "white" and self.deadOnce == True:

			self.setStyleSheet("background: silver")
			self.color = "silver" 
			self.model.setCellInactive(self.i , self.j )

			self.aliveCells.updateInfoLabel(self.model.getAliveCells())

		else:

			print('Cell is already occupied.')


	def setColor(self, color):
		""" Method to set the Color of a cell """
		self.setStyleSheet('background: ' + color)
		self.color = color

	def getColor(self):
		""" Method that get the color of a cell """
		return self.color

	def setDeadOnce(self, value):
		""" Method to set the 'deadOnce' attribute as True or False """
		self.deadOnce = value

class GameOfLifeBoard(QGridLayout):
	""" Custom Grid that contains all the tiles representing the cells.

		Attributes:
			model       reference to the model
			tileList    auxiliary list containing the references to the tiles, so that to speed up the color change of the tiles, passing from a state to the next
			notBlack    matrix used to keep track of tiles that are not black. It is used to update the Board, when clear mode is requested
			aliveCells  reference to the label that display the number of alive cells
	""" 
	def __init__(self, model, aliveCellsLabel):
		""" Init method """
		super().__init__()

		self.model = model
		self.tileList = []
		self.notBlack = np.zeros((50,86))
		self.aliveCells = aliveCellsLabel
		self.setVerticalSpacing(0)
		self.setHorizontalSpacing(0)
		for i in range(0,50):#rows
			for j in range(0,86):#columns
				aButton = GameOfLifeTile(i,j,self.model,self.notBlack, self.aliveCells)
				self.addWidget(aButton,i,j)
				self.tileList.append(aButton)

	def getTile(self, i, j):
		""" Method to get the tile at position (i,j) """
		return self.tileList[i+j]

	def updateView(self, currentState, newState, mode):
		""" Method used to update the board. For this method there are three different modes ('clear' if user wants to clear the board, 
		'nextStep' to compute the next state of Game of Life, 'load' to load a known pattern). 
		To speed up the update, this implementation take advantages from sparsity of the model. """
		if mode == 'clear':
			findNotBlack = self.notBlack == 1
			indices = np.argwhere(findNotBlack == True)
			for el in indices:
				i,j = el
				self.getTile(i*86, j).setColor('black')
				self.getTile(i*86, j).setDeadOnce(False)
				self.notBlack[i,j] = 0
		elif mode == 'nextStep':
			findDifferences = newState != currentState
			indices = np.argwhere(findDifferences == True)
			for el in indices:
				i, j = el

				#dying cells
				if self.getTile(i*86, j).getColor() == 'white' or self.getTile(i*86, j).getColor() == 'lime' or self.getTile(i*86, j).getColor() == 'green':
					self.getTile(i*86, j).setColor('silver')
					self.getTile(i*86, j).setDeadOnce(True)
					if self.notBlack[i,j] == 0:
						self.notBlack[i,j] = 1
				#borning cells
				elif self.getTile(i*86, j).getColor() == 'silver' or self.getTile(i*86, j).getColor() == 'black':
					self.getTile(i*86, j).setColor('lime')
					if self.notBlack[i,j] == 0:
						self.notBlack[i,j] = 1

			#old cells
			findEqualities = newState + currentState
			indices = np.argwhere(findEqualities == 2)
			for el in indices:
				i,j = el
				self.getTile(i*86, j).setColor('green')
				if self.notBlack[i,j] == 0:
						self.notBlack[i,j] = 1
		elif mode == 'load':
			findDifferences  = newState != currentState
			indices = np.argwhere(findDifferences == True)
			for el in indices:
				i, j = el
				self.getTile(i*86, j).setColor('white')
				if self.notBlack[i,j] == 0:
					self.notBlack[i,j] = 1


		


