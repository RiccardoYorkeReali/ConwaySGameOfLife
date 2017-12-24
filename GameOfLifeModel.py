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

import numpy as np
import scipy.ndimage as spndmg

## THE MODEL

class GameOfLifeModel:
	"""
    This class represents the Model of the game. 
    It contains the states and the implementation of the game's rules.
    It provides a method to compute the evolution of states, based on the rules of the game (nextState),
    methods to get and set the values of the class' attributes, and the methods to clear, load and save the state.

    Attributes:
        cells             the current state of the Game.
        aliveCells        the number of alive cells.
        generation        the current generation in which current State's cells live.
    """

	def __init__(self):
		""" Init method """
		self.cells = np.zeros((50,86))
		self.aliveCells = np.sum(self.cells == 1)
		self.generation = 0

	def setCellActive(self, i, j):
		""" Method to set the (i,j)-th cell active """
		self.cells[i, j] = 1
		self.aliveCells = np.sum(self.cells == 1)

	def setCellInactive(self, i, j):
		""" Method to set the (i,j)-th inactive """
		self.cells[i, j] = 0
		self.aliveCells = np.sum(self.cells == 1)

	def getAliveCells(self):
		""" Method to get the number of alive cells """
		return self.aliveCells

	def getCurrentState(self):
		""" Method to get the current state of the Game """
		return self.cells

	def getGeneration(self):
		""" Method to get the generation in which current State's cells live """
		return self.generation

	def nextState(self):
		""" Method to compute the next Game's state. It is based on convolution """
		kernel = np.array([[1,1,1], [1,50,1], [1,1,1]])
		convolution = spndmg.filters.convolve(self.cells, kernel, mode = 'constant', cval = 0)
		self.cells = np.int8((convolution == 3) | (convolution == 53) | (convolution == 52))
		self.aliveCells = np.sum(self.cells == 1)
		self.generation = self.generation + 1
		return self.cells

	def clearModel(self):
		""" Method to clear the Model. It reinitialize all the attributes to the initial state """
		self.cells = np.zeros((50,86))
		self.aliveCells = np.sum(self.cells == 1)
		self.generation = 0
		return self.cells

	def saveModel(self, title):
		""" Method to save an own Pattern. It requires a string which is used as the title of the pattern """
		path = 'myPatterns/'
		directory = os.path.dirname(path)
		if not os.path.exists(directory):
			os.makedirs(directory)
		path = path + title
		np.save(path, self.cells)

	def loadModel(self, path, pattern):
		""" Method to load a Pattern. It requires a string representing the path needed to get the pattern, and the title of the pattern """
		self.cells = np.load(path + pattern)
		self.aliveCells = np.sum(self.cells == 1)
		return self.cells