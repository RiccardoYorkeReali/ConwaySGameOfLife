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

import sys

from PyQt5.QtWidgets import QApplication 

from GameOfLifeModel import GameOfLifeModel
from MainWindow import MainWindow

if __name__ == '__main__':

	#Loading the style
    file_object  = open('QTDark.stylesheet', 'r')
    style = file_object.read()

    app = QApplication(sys.argv)
    app.setStyleSheet(style)

	#The Model
    model = GameOfLifeModel() 

    #The View and Controller
    window = MainWindow(model) 
    window.setStyleSheet(style)
    sys.exit(app.exec_())
