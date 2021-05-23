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

import collections

# austin's shortcut notes:
# python src/Main.py -d -f ../WorldGenerator/Problems/
# cd Documents/uci/Spring 2021/CS171/minesweeper/Minesweeper_Student-master/Minesweeper_Python


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
		self.numFlaggedTiles:int = 0
		self.totalTimeElapsed:float = 0.0
		self.totalMines:int = totalMines
		
		# print("row dimension: ", rowDimension)
		# print("col dimension: ", colDimension)

		# Instantiate action queue
		self.actionQueue = collections.deque()

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

		# Specific Tile Definitions
		numFlaggedNeighbors:int = 0
		numCoveredNeighbors:int = 8
		singleUncoveredTileX:int = -1
		singleUncoveredTileY:int = -1
		# effectiveLabel = tileLabel - numFlaggedNeighbors

		prevMoveX:int = self.currentAction.getX()
		prevMoveY:int = self.currentAction.getY()
		prevMoveAction:str = self.currentAction.getMove()


		if (prevMoveAction == AI.Action.FLAG):
			self.numFlaggedTiles += 1

		# Check if goal reached
		if (self.numFlaggedTiles == self.totalMines):
			return Action(AI.Action.LEAVE)

		if (prevMoveAction == AI.Action.UNCOVER):
			# add previous tile to uncovered
			self.uncoveredTiles.add((prevMoveX, prevMoveY))
			
			# update board to previous tile
			self.msBoard.updateBoard(prevMoveX, prevMoveY, number)
			self.coveredTiles -= 1

			# basic case: 0 tile
			if (number == 0):
				# check surrounding neighbors to uncover if covered
				for i in range(-1,2):
					for j in range(-1,2):
						if (self.validBounds(prevMoveX + i, prevMoveY + j)) and self.msBoard.checkBoard(prevMoveX + i, prevMoveY + j) == -1:
							if ((prevMoveX + i, prevMoveY + j) not in self.uncoveredTiles):
								self.uncoveredTiles.add((prevMoveX + i, prevMoveY + j))
								self.actionQueue.append(Action(AI.Action.UNCOVER, prevMoveX + i, prevMoveY + j))
	

			# basic case: 1 tile
			if (number == 1):
				# check surrounding neighbors to see whats covered
				# if only one tile is uncovered -> flag it
				# else, ignore this tile and continue (basically go around this 1 tile and continue until complete)
				for i in range(-1,2):
					for j in range(-1,2):
						if i == 0 and j == 0:
							continue
						if (self.validBounds(prevMoveX + i, prevMoveY + j)) == False or self.msBoard.checkBoard(prevMoveX + i, prevMoveY + j) != -1:
							numCoveredNeighbors -= 1

						else:
							singleUncoveredTileX = prevMoveX + i
							singleUncoveredTileY = prevMoveY + j

				# if only one covered tile -> flag
				if (numCoveredNeighbors == 1):
					if (Action(AI.Action.FLAG, singleUncoveredTileX, singleUncoveredTileY) not in self.actionQueue):
						if ((prevMoveX + i, prevMoveY + j) not in self.uncoveredTiles):
							self.uncoveredTiles.add((prevMoveX + i, prevMoveY + j))
							self.actionQueue.append(Action(AI.Action.FLAG, singleUncoveredTileX, singleUncoveredTileY))


			# case: tile > 1
			if (number > 1):
				# effectiveLabel: number of bombs left in neighboring tiles
				effectiveLabel:int = number

				# list of tuple coordinates of covered neighboring tiles
				coveredTiles:list = []

				for i in range(-1, 2):
					for j in range(-1, 2):
						if i == 0 and j == 0:
							continue
						# if tile is uncovered or not on board (off the board), reduce covered neighbors count
						if (self.validBounds(prevMoveX + i, prevMoveY + j)) == False or self.msBoard.checkBoard(prevMoveX + i, prevMoveY + j) != -1:
							numCoveredNeighbors -= 1
						elif (self.validBounds(prevMoveX + i, prevMoveY + j) == True):
							# if tile is already flagged, change effective label
							if (self.msBoard.checkBoard(prevMoveX + i, prevMoveY + j) == -2):
								effectiveLabel -= 1
							
							# if tile is covered and on the board, add the tile's coords to list
							elif (self.msBoard.checkBoard(prevMoveX + i, prevMoveY + j) == -1):
								coveredTiles.append((prevMoveX + i, prevMoveY + j))


				# if number of covered neighbor tiles 
				if (numCoveredNeighbors == effectiveLabel):
					for tile in coveredTiles:
						self.actionQueue.append(Action(AI.Action.FLAG, tile[0], tile[1]))

		

		# if action queue is empty, recheck
		if len(self.actionQueue) == 0:
			# find remaining covered tile
			coveredCoords:tuple = self.msBoard.findCoveredTile()

			# HARD CODED FOR SUPEREASY: remaining tile should be the bomb
			self.actionQueue.append(Action(AI.Action.FLAG, coveredCoords[0], coveredCoords[1]))



		# DEBUGGING PRINT
		# for value in self.actionQueue:
		# 	print(value.getMove(), value.getX(), value.getY())
		
		# get next action in queue
		self.currentAction = self.actionQueue.popleft()

		print("NEXT MOVE: ", self.currentAction.getMove(), self.currentAction.getX(), self.currentAction.getY())

		return self.currentAction

	
	def validBounds(self, xvalue: int, yvalue: int) -> bool:
		''' return boolean to check if tile is within board boundaries'''
		if xvalue in range (0, self.colDimension) and yvalue in range(0, self.rowDimension):
			return True
		else:
			# print("col dimension: ", self.colDimension, " xvalue: ", xvalue)
			# print("row dimension: ", self.rowDimension, " yvalue: ", yvalue)
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
		self.colDimension = colDimension
		self.rowDimension = rowDimension

		# Board States: 
		# -2 : flagged
		# -1 : covered / unknown
		# 0 : empty tile with no bombs in neighborhood
		# 1-8 : number of bombs in neighborhood

		self.tileStates = set(range(-2, 8))
 
		# create fully covered board
		self.board = [[-1 for index in range(colDimension)] for index in range(rowDimension)]
		self.totalMines = totalMines

		self.board[startX, startY] = 0


	def updateBoard(self, positionX, positionY, tileValue):
		''' pass in action at certain position and update board '''
		self.board[positionX, positionY] = tileValue

	def checkBoard(self, positionX, positionY) -> int:
		''' return tileValue at position '''
		return self.board[positionX, positionY]
	
	def printBoard(self):
		''' debugging purposes - print full board '''
		print(self.board)

	def findCoveredTile(self) -> tuple:
		''' find a random covered tile on the board and return tuple of coordinates'''
		for row in range(0, self.colDimension):
			for col in range(0, self.rowDimension):
				if self.board[row, col] == -1:
					return (row, col)
		
		# if no covered tiles found
		# this should never happen
		return (-1, -1)


		






