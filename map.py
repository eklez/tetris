#!/usr/bin/python3
import numpy as np

class MainMap:
    MAX_WIDTH=22
    MAX_HEIGHT=22
    MAX_UNIT=40
    MAX_UNION=10000

    def __init__(self):
        self.score = 0
        self.curWidth = 0
        self.curHeigth = 0
        self.mapArray = np.zeros([MainMap.MAX_WIDTH,MainMap.MAX_HEIGHT,3])
        self.union = 0
        self.unionLev = 0
        self.curUnit = 0
        self.mapMaxUnit = 0

    def calcscore(self):
        return self.score

    def isslotpossible (self, row, column):
        return self.mapArray[row, column, 1]
    def isslotoccupy (self, row, column):
        return self.mapArray[row, column, 2]

    def initialize(self, union):
        if union > MainMap.MAX_UNION:
            union = MainMap.MAX_UNION

        self.score = 0
        self.curUnit = 0
        self.union = union
        self.unionLev = self.union / 500

        # Max Unit
        if self.unionLev < 5:
            self.mapMaxUnit = 9 + self.unionLev
        elif self.unionLev < 10:
            self.mapMaxUnit = 18 + (self.unionLev - 5)
        elif self.unionLev < 15:
            self.mapMaxUnit = 27 + (self.unionLev - 10)
        else:
            self.mapMaxUnit = 36 + (self.unionLev - 15)

        # Width / Height
        if self.unionLev >= 12:
            self.curWidth = 22
            self.curHeight = 22
        elif self.unionLev >= 10:
            self.curWidth = 20
            self.curHeight = 20
        elif self.unionLev >= 8:
            self.curWidth = 18
            self.curHeight = 18
        elif self.unionLev >= 6:
            self.curWidth = 16
            self.curHeight = 16
        elif self.unionLev >= 4:
            self.curWidth = 14
            self.curHeight = 14
        else:
            self.curWidth = 10
            self.curHeight = 10

        # Initialize Map
        emptyline = int ((MainMap.MAX_WIDTH - self.curWidth)/2)
        for i in range (emptyline, MainMap.MAX_HEIGHT-emptyline):
            for j in range (emptyline, MainMap.MAX_WIDTH-emptyline):
                # Set current slot is possible
                self.mapArray[i,j,1] = 1
                # Set section of map
                if i >= j and i < (MainMap.MAX_WIDTH-j) and i < 11 and j < 11:
                    self.mapArray[i,j,0] = 0
                    if j > 5:
                        self.mapArray[i,j,0] += 1
                elif i >= j and i < (MainMap.MAX_WIDTH-j) and i >= 11 and j < 11:
                    self.mapArray[i,j,0] = 2
                    if j > 5:
                        self.mapArray[i,j,0] += 1
                elif i >= j and i >= (MainMap.MAX_WIDTH-j) and i >= 11 and j < 11:
                    self.mapArray[i,j,0] = 4
                    if i < 17:
                        self.mapArray[i,j,0] += 1
                elif i >= j and i >= (MainMap.MAX_WIDTH-j) and i >= 11 and j >= 11:
                    self.mapArray[i,j,0] = 6
                    if i < 17:
                        self.mapArray[i,j,0] += 1
                elif i < j and i >= (MainMap.MAX_WIDTH-j) and i >= 11 and j >= 11:
                    self.mapArray[i,j,0] = 8
                    if j < 17:
                        self.mapArray[i,j,0] += 1
                elif i < j and i >= (MainMap.MAX_WIDTH-j) and i < 11 and j >= 11:
                    self.mapArray[i,j,0] = 10
                    if j < 17:
                        self.mapArray[i,j,0] += 1
                elif i < j and i < (MainMap.MAX_WIDTH-j) and i < 11 and j >= 11:
                    self.mapArray[i,j,0] = 12
                    if i > 5:
                        self.mapArray[i,j,0] += 1
                elif i < j and i < (MainMap.MAX_WIDTH-j) and i < 11 and j < 11:
                    self.mapArray[i,j,0] = 14
                    if i > 5:
                        self.mapArray[i,j,0] += 1
                else:
                    print ("Couldn't be here i : %d j : %d" %(i,j))

                print ("%02d  " %(self.mapArray[i,j,0]), end='')
            print ("")






            
