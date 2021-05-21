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

# import numpy as np
import queue
import collections


# austin's shortcut notes:
# python src/Main.py -d -f ../WorldGenerator/Problems/
# cd Documents/uci/Spring 2021/CS171/minesweeper/Minesweeper_Student-master/Minesweeper_Python


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        ########################################################################
        #							YOUR CODE BEGINS						   #
        ########################################################################

        # Instantiate an array representation of the board
        self.msBoard = Board(rowDimension, colDimension, totalMines, startX, startY)
        self.rowDimension = rowDimension  # y-value
        self.colDimension = colDimension  # x-value

        self.coveredTiles: int = rowDimension * colDimension
        self.numFlaggedTiles: int = 0
        self.totalTimeElapsed: float = 0.0
        self.totalMines: int = totalMines

        # print("row dimension: ", rowDimension)
        # print("col dimension: ", colDimension)

        # Instantiate action queue
        self.actionQueue = collections.deque()

        # Instantiate discovered / uncovered set
        self.uncoveredTiles = set()
        self.uncoveredTiles.add((startX, startY))
        self.currentQueue = set()
        self.flaggedSpots = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.validBounds(startX + i, startY + j) and self.msBoard.checkBoard(startX + i, startY + j) == -1 and (startX + i, startY + j) not in self.uncoveredTiles and (startX + i, startY + j) not in self.currentQueue:
                    self.actionQueue.append(Action(AI.Action.UNCOVER, startX + i, startY + j))
                    self.currentQueue.add((startX + i, startY + j))
        self.flaggedEffectiveCount = dict()

        self.numFlags: int = 0

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


        self.msBoard.printBoard()
        if len(self.uncoveredTiles) == (self.colDimension * self.rowDimension) - 1:
            return Action(AI.Action.LEAVE, 1, 1)


        else:
            # Specific Tile Definitions
            #numFlaggedNeighbors: int = 0
            #numCoveredNeighbors: int = 8
            #singleUncoveredTileX: int = -1
            #singleUncoveredTileY: int = -1
            # effectiveLabel = tileLabel - numFlaggedNeighbors

            #update effective label
            #print("uncovered tiles: ",self.uncoveredTiles)
            if len(self.flaggedSpots) != 0:


                for flags in self.flaggedSpots:
                    for i in range(-1, 2):
                        for j in range(-1, 2):

                            if self.validBounds(flags[0] + i,flags[1] + j) and (flags[0] + i, flags[1] + j) not in self.flaggedEffectiveCount[(flags[0], flags[1])] and self.msBoard.checkBoard(flags[0] + i,flags[1] + j)  > -1:
                                self.flaggedEffectiveCount[(flags[0], flags[1])].add((flags[0] + i, flags[1] + j))
                                current_value = self.msBoard.checkBoard(flags[0] + i, flags[1] + j)
                                self.msBoard.updateBoard(flags[0] + i, flags[1] + j, current_value - 1)

                                if current_value == 1:
                                    _x = flags[0] + i
                                    _y = flags[1] + j
                                    for k in range(-1, 2):
                                        for l in range(-1, 2):
                                            if k == 0 and l == 0:
                                                continue
                                            if self.validBounds(_x + k, _y + l) and self.msBoard.checkBoard(_x + k, _y + l) == -1 and (_x + k, _y + l) not in self.currentQueue and (_x + k, _y + l) not in self.flaggedEffectiveCount[(flags[0], flags[1])] and (_x + k, _y + l) not in self.uncoveredTiles and (_x + k, _y + l) != (self.currentAction.getX(), self.currentAction.getY()):
                                                self.currentQueue.add((_x + k, _y + l))
                                                self.actionQueue.append(Action(AI.Action.UNCOVER,_x + k, _y + l))


            prevMoveX: int = self.currentAction.getX()
            prevMoveY: int = self.currentAction.getY()
            prevMoveAction = self.currentAction.getMove()


            if (prevMoveAction == AI.Action.UNCOVER):


                # update board to previous tile
                self.msBoard.updateBoard(prevMoveX, prevMoveY, number)
                self.coveredTiles -= 1

                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (self.validBounds(prevMoveX + i, prevMoveY + j)) and self.msBoard.checkBoard(prevMoveX + i, prevMoveY + j) == -1 and ((prevMoveX + i, prevMoveY + j) not in self.uncoveredTiles and (prevMoveX + i, prevMoveY + j) not in self.currentQueue) and self.msBoard.checkBoard(prevMoveX,prevMoveY) == 0:
                            self.actionQueue.append(Action(AI.Action.UNCOVER, prevMoveX + i, prevMoveY + j))
                            self.currentQueue.add((prevMoveX + i, prevMoveY + j))


                    # check surrounding neighbors to see whats covered
                    # if only one tile is uncovered -> flag it
                    # else, ignore this tile and continue (basically go around this 1 tile and continue until complete)
                new_corners = self.cornerChecker()

                if len(new_corners) != 0:
                    for element in new_corners:
                        if (element[0],element[1]) not in self.currentQueue and (element[0],element[1]) not in self.uncoveredTiles:
                            self.actionQueue.appendleft(Action(AI.Action.FLAG,element[0],element[1]))
                            self.currentQueue.add((element[0], element[1]))

            # Flag is hardcoded for SuperEasy Worlds #####################################
            if (prevMoveAction == AI.Action.FLAG):
                self.coveredTiles -= 1

                self.numFlaggedTiles += 1

            self.currentAction = self.actionQueue.popleft()
            self.currentQueue.remove((self.currentAction.getX(), self.currentAction.getY()))
            self.uncoveredTiles.add((prevMoveX, prevMoveY))

            return self.currentAction

    def validBounds(self, xvalue: int, yvalue: int) -> bool:
        ''' return boolean to check if tile is within board boundaries'''
        if xvalue in range(0, self.colDimension) and yvalue in range(0, self.rowDimension):
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


    def cornerChecker(self):
        new_corners = list()
        for _x in range(self.colDimension):
            for _y in range(self.rowDimension):
                numCoveredNeighbors = 8
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if (self.validBounds(_x + i, _y + j)) == False:
                            numCoveredNeighbors -= 1
                        elif (self.msBoard.checkBoard(_x + i, _y + j) > -1 and self.msBoard.checkBoard(_x , _y) > -1):
                            numCoveredNeighbors -= 1
                if self.msBoard.checkBoard(_x, _y) > 0 and numCoveredNeighbors == self.msBoard.checkBoard(_x,_y):
                    new_corners.append((_x, _y))

        return_list = []
        for element in new_corners:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if self.validBounds(element[0] + i,element[1] + j) and self.msBoard.checkBoard(element[0] + i, element[1] + j) == -1 and (element[0] + i, element[1] + j) not in self.flaggedSpots:
                        return_list.append((element[0] + i,element[1] + j))
                        self.flaggedSpots.add((element[0] + i, element[1] + j))
                        self.msBoard.updateBoard(element[0] + i, element[1] + j, -2)
                        self.flaggedEffectiveCount[(element[0] + i, element[1] + j)] = set()
                        self.actionQueue.appendleft(Action(AI.Action.FLAG, element[0] + i, element[1] + j))
                        self.currentQueue.add((element[0] + i, element[1] + j))
        return return_list


class Board:
    ''' Keep track of the Minesweeper Gameboard'''

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        # Simulate the board with an array

        # Board States:
        # -2 : flagged
        # -1 : covered / unknown
        # 0 : empty tile with no bombs in neighborhood
        # 1-8 : number of bombs in neighborhood

        self.tileStates = set(range(-2, 8))

        # create fully covered board
        self.board = [[-1 for index in range(colDimension)] for index in range(rowDimension)]
        self.totalMines = totalMines

        self.board[startX][startY] = 0

    def updateBoard(self, positionX, positionY, tileValue):
        ''' pass in action at certain position and update board '''
        # print("updated ", positionX, positionY, tileValue)
        self.board[positionX][positionY] = tileValue

    # print(self.board)

    def checkBoard(self, positionX, positionY) -> int:
        ''' return tileValue at position '''
        return self.board[positionX][positionY]

    def printBoard(self):
        ''' debugging purposes - print full board '''
        for _x in range(len(self.board)):
            for _y in range(len(self.board[0])):
                print(" ", self.board[_x][_y], " ", end='')
            print()


