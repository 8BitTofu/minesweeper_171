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

import random
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



        # Instantiate action queue
        self.actionQueue = collections.deque()

        # Instantiate discovered / uncovered set
        self.uncoveredTiles = set()
        self.uncoveredTiles.add((startX, startY))
        self.currentQueue = set()
        self.flaggedSpots = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.validBounds(startX + i, startY + j):
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


        #self.msBoard.printBoard()
        if len(self.uncoveredTiles) == (self.colDimension * self.rowDimension) - 1:
            return Action(AI.Action.LEAVE, 1, 1)


        else:
            # Specific Tile Definitions
            #numFlaggedNeighbors: int = 0
            #numCoveredNeighbors: int = 8
            #singleUncoveredTileX: int = -1
            #singleUncoveredTileY: int = -1
            # effectiveLabel = tileLabel - numFlaggedNeighbors

            # self.msBoard.printBoard()

            #print("FLAGS", self.flag_checker())
            prevMoveX: int = self.currentAction.getX()
            prevMoveY: int = self.currentAction.getY()
            prevMoveAction = self.currentAction.getMove()
            self.msBoard.updateBoard(prevMoveX, prevMoveY, number)
            self.coveredTiles -= 1

            

            if len(self.flaggedSpots) != 0:
                # update effective label
                # print("updated flags")
                self.update_effective_number()


            if (prevMoveAction == AI.Action.UNCOVER):

                # update board to previous tile
                length_of_queue =  len(self.currentQueue)
                """
                self.msBoard.updateBoard(prevMoveX, prevMoveY, number)
                self.coveredTiles -= 1
                """

                self.add_safe_spots(prevMoveX,prevMoveY)
                new_corners = self.cornerChecker()
                """ 
                if len(new_corners) != 0:
                    for element in new_corners:
                        if (element[0],element[1]) not in self.currentQueue and (element[0],element[1]) not in self.uncoveredTiles:
                            self.actionQueue.appendleft(Action(AI.Action.FLAG,element[0],element[1]))
                            self.currentQueue.add((element[0], element[1]))                    
                        


                """

                #if length_of_queue == len(self.currentQueue):
                    #self.flag_checker()
                #print("new_corners",new_corners)

            if (prevMoveAction == AI.Action.FLAG):
                self.coveredTiles -= 1
                self.numFlaggedTiles += 1
                self.msBoard.updateBoard(self.currentAction.getX(), self.currentAction.getY(), -2) # flag the board


            # if action queue is empty do these
            if len(self.actionQueue) == 0:
                # print("NO MORE QUEUE")                
                flags:list = self.flag_checker()


            # if previous method didnt work -> try this
            # last resort -> pick a random covered tile and uncover
            if len(self.actionQueue) == 0:
                # print("LAST RESORT")
                tile:tuple = self.msBoard.getRandomCoveredTile()
                self.actionQueue.append(Action(AI.Action.UNCOVER, tile[0], tile[1]))
                self.currentQueue.add((tile[0], tile[1]))


            frontier_list = self.frontier()
            print("Frontier List",frontier_list)
            print("Queue",self.currentQueue)
            print("actionQueue: ")
            for action in self.actionQueue:
                print(str(action.getMove()) + " at (" + str(action.getX()) + "," + str(action.getY()) + ")")

            self.currentAction = self.actionQueue.popleft()

            # print("remove: ", self.currentAction.getX(), self.currentAction.getY())

            self.currentQueue.remove((self.currentAction.getX(), self.currentAction.getY()))
            self.uncoveredTiles.add((prevMoveX, prevMoveY))

            print("next action: " + str(self.currentAction.getMove()) + " at (" + str(self.currentAction.getX()) + "," + str(self.currentAction.getY()) + ")")
            return self.currentAction
                


    def validBounds(self, xvalue: int, yvalue: int) -> bool:
        ''' return boolean to check if tile is within board boundaries'''
        if xvalue in range(0, self.colDimension) and yvalue in range(0, self.rowDimension):
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
                        elif ((self.msBoard.checkBoard(_x + i, _y + j) > -1 or self.msBoard.checkBoard(_x + i, _y + j) == -2) and self.msBoard.checkBoard(_x , _y) > -1):
                            numCoveredNeighbors -= 1
                if self.msBoard.checkBoard(_x, _y) > 0 and numCoveredNeighbors == self.msBoard.checkBoard(_x,_y):
                    new_corners.append((_x, _y))
        #print("new corners inside func",new_corners)
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

    def add_safe_spots(self, prevMoveX, prevMoveY):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (self.validBounds(prevMoveX + i, prevMoveY + j)) and self.msBoard.checkBoard(prevMoveX + i,
                                                                                                prevMoveY + j) == -1 \
                        and ((prevMoveX + i, prevMoveY + j) not in self.uncoveredTiles and (
                prevMoveX + i, prevMoveY + j) not in self.currentQueue) \
                        and self.msBoard.checkBoard(prevMoveX, prevMoveY) == 0:
                    self.actionQueue.append(Action(AI.Action.UNCOVER, prevMoveX + i, prevMoveY + j))
                    self.currentQueue.add((prevMoveX + i, prevMoveY + j))


    def update_effective_number(self):
        for flags in self.flaggedSpots:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.validBounds(flags[0] + i, flags[1] + j) and (flags[0] + i, flags[1] + j) not in \
                            self.flaggedEffectiveCount[(flags[0], flags[1])] \
                            and self.msBoard.checkBoard(flags[0] + i, flags[1] + j) > -1:
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
                                    if self.validBounds(_x + k, _y + l) and self.msBoard.checkBoard(_x + k,
                                                                                                    _y + l) == -1 \
                                            and (_x + k, _y + l) not in self.currentQueue and (_x + k, _y + l) not in \
                                            self.flaggedEffectiveCount[(flags[0], flags[1])] \
                                            and (_x + k, _y + l) not in self.uncoveredTiles and (_x + k, _y + l) != (
                                    self.currentAction.getX(), self.currentAction.getY()):
                                        self.currentQueue.add((_x + k, _y + l))
                                        self.actionQueue.append(Action(AI.Action.UNCOVER, _x + k, _y + l))

    def frontier(self):
        frontier_list = list()
        for _x in range(self.rowDimension):
            for _y in range(self.colDimension):
                #Check if only one side is unknown Only checking right, left, up down
                list_of_adjacent = list()
                number_of_valid_sides = 0

                for i in range(-1,2):
                    for j in range(-1,2):
                        if i == 0 and j == 0:
                            continue
                        elif self.validBounds(_x + i, _y + j):
                            # if _x == 0 and _y == 1:
                                # print("(" + str(_x + i) + "," + str(_y + j) + "): " + str(self.msBoard.checkBoard(_x + i, _y + j)))
                            list_of_adjacent.append(self.msBoard.checkBoard(_x + i, _y + j))
                            number_of_valid_sides += 1
                
                
                # if self.validBounds(_x - 1, _y):
                #     list_of_adjacent.append(self.msBoard.checkBoard(_x - 1, _y))
                #     number_of_valid_sides += 1
                # if self.validBounds(_x + 1, _y):
                #     list_of_adjacent.append(self.msBoard.checkBoard(_x + 1, _y))
                #     number_of_valid_sides += 1
                # if self.validBounds(_x, _y - 1):
                #     list_of_adjacent.append(self.msBoard.checkBoard(_x, _y - 1))
                #     number_of_valid_sides += 1
                # if self.validBounds(_x, _y + 1):
                #     list_of_adjacent.append(self.msBoard.checkBoard(_x, _y + 1))
                #     number_of_valid_sides += 1

                number_of_unknown = 0
                for element in list_of_adjacent:
                    if element == -1:
                        number_of_unknown += 1
                
                # if _x == 0 and _y == 1:
                    # print("number of unknown: ", number_of_unknown)

                if number_of_unknown >= 1 and number_of_unknown < number_of_valid_sides and self.msBoard.checkBoard(_x,_y) != -1:
                    frontier_list.append((_x, _y))
        return frontier_list



    def flag_checker(self):
        new_flags = []
        for _x in range(self.colDimension):
            for _y in range(self.rowDimension):
                numCoveredNeighbors = 8
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if (self.validBounds(_x + i, _y + j)) == False:
                            numCoveredNeighbors -= 1
                        elif ((self.msBoard.checkBoard(_x + i, _y + j) > -1 or self.msBoard.checkBoard(_x + i, _y + j) == -2) and self.msBoard.checkBoard(_x, _y) > -1):
                            numCoveredNeighbors -= 1
                if self.msBoard.checkBoard(_x, _y) > 0 and numCoveredNeighbors == self.msBoard.checkBoard(_x, _y):
                    new_flags.append((_x, _y))
                """
                if _x == 4 and _y == 4:
                    print("x == 4, y == 4"," value ",self.msBoard.checkBoard(_x,_y),"numCovered",numCoveredNeighbors)
                """
        for _x, _y in new_flags:
            for i in range(-1,2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if self.msBoard.checkBoard(_x + i,_y + j) == -1:
                        self.flaggedSpots.add((_x + i, _y + j))
                        self.msBoard.updateBoard(_x + i, _y + j, -2)
                        self.flaggedEffectiveCount[(_x + i, _y + j)] = set()
                        self.actionQueue.append(Action(AI.Action.FLAG, _x + i, _y + j))
                        self.currentQueue.add((_x + i, _y + j))


        return new_flags







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
        self.board = [[-1 for index in range(rowDimension)] for index in range(colDimension)]
        self.totalMines = totalMines
        self.colDimension = colDimension
        self.rowDimension = rowDimension

        # in theory: 
        # row is y / # of rows = rowDimension
        # col is x / # of cols = colDimension


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

    def getRandomCoveredTile(self) -> tuple:
        ''' return coordinates of a random covered tile '''
        tileCovered = False
        
        while tileCovered == False:
            randomX = random.randint(0, self.colDimension - 1)
            randomY = random.randint(0, self.rowDimension - 1)

            if self.checkBoard(randomX, randomY) == -1:
                return (randomX, randomY)




