# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action

import numpy as np
import queue



class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		# Instantiate an array representation of the board
		self.msBoard = Board(rowDimension, colDimension, totalMines, startX, startY)
		self.rowDimension = rowDimension # y-value
		self.colDimension = colDimension # x-value

		self.coveredTiles:int = rowDimension*colDimension
		self.totalTimeElapsed:float = 0.0
		self.totalMines:int = totalMines
		

		# Instantiate action queue
		self.actionQueue = queue.Queue()

		# Instantiate discovered / uncovered set
		self.uncoveredTiles = set()
		self.numFlags:int = 0

		# Make initial first move on board
		self.currentAction = Action(AI.Action.UNCOVER, startX, startY)
		self.coveredTiles -= 1




		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		# Check if goal reached
		if (self.coveredTiles == self.totalMines):
			return Action(AI.Action.LEAVE)

		else:
			# Specific Tile Definitions
			numFlaggedNeighbors = -1
			numCoveredNeighbors = 8
			tileLabel = -1 ## tile number (i.e. 0-8)
			# effectiveLabel = tileLabel - numFlaggedNeighbors

			if (number != -1):
				prevMoveX = self.currentAction.getX()
				prevMoveY = self.currentAction.getY()
				prevMoveAction = self.currentAction.getMove()

				# basic case: 0 tile
				if (prevMoveAction == "UNCOVER"):
					self.uncoveredTiles.add((prevMoveX, prevMoveY))
					self.coveredTiles -= 1

					if (number == 0):
						# check surrounding neighbors to uncover if covered
						for i in range(-1,2):
							for j in range(-1,2):
								if (self.validBounds(prevMoveX + i, prevMoveY + j)) and
								(prevMoveX + i, prevMoveY + j) not in self.uncoveredTiles:
										self.actionQueue.put(Action(AI.Action.UNCOVER, prevMoveX + i, prevMoveY + j))

	
	def validBounds(self, xvalue: int, yvalue: int) -> bool:
		''' return boolean to check if tile is within board boundaries'''
		if (xvalue <= self.colDimension) and (xvalue > 0) and (yvalue <= self.rowDimension) and (yvalue > 0):
			return True
		else:
			return False


					






			# RULE OF THUMBS NOTES
			# 1) if effectiveLabel == numCoveredNeighbors: 
			# ->		flag all the covered neighbors

			# 2) if titleLabel = 0: 
			# ->		flag all covered neighbors



			# more specific rules

			# *) if effectiveLabel == 2 && 
			# ([adjacent neighbors are NS] || [adjacent neighbors are WE]) &&
			# [these adjacent neighbors' effectiveLabels BOTH == 1] && 
			# numCoveredNeighbors == 3 &&
			# [these covered neighbors are all adjacent in NSWE (basically mirroring the three we are looking at)]:
			# ->		flag tiles that are on opposite ends of the current tile
			# EX:
			# - 1 F
			# - 2 -
			# - 1 F
			
			# *) if effectiveLabel == 1 && numCoveredNeighbors == 2 && 
			# [covered neighbors are directly adjacent NSWE] &&
			# [one of these covered neighbors' numCoveredNeighbors > 1] && 
			# [other covered neighbors' numCoveredNeighbors == 1]: 
			# ->		flag the neighbor that has numCoveredNeighbors == 1



		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	
class Board:
	''' Keep track of the Minesweeper Gameboard'''

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		# Simulate the board with an array

		# Board States: 
		# -2 : flagged
		# -1 : covered / unknown
		# 0 : empty tile with no bombs in neighborhood
		# 1-8 : number of bombs in neighborhood

		self.uncoveredTileRange = set(range(-2, 8))
 
		# create fully covered board
		self.board = np.full((colDimension, rowDimension), fill_value = -1)
		self.totalMines = totalMines

		self.board[startX, startY] = 0


	def updateBoard(self, positionX, positionY, tileValue):
		''' pass in action at certain position and update board '''
		pass
		






