#!/usr/bin/python3
import numpy as np
import copy
from block import Block

class MainMap:
    MAX_WIDTH=22
    MAX_HEIGHT=20
    MAX_UNIT=40
    MAX_UNION=10000

    def __init__(self):
        self.score = 0
        self.curWidth = 0
        self.curHeigth = 0
        # For Bump
        self.mapArray = np.zeros([MainMap.MAX_HEIGHT+8,MainMap.MAX_WIDTH+8,3])
        self.union = 0
        self.unionLev = 0
        self.curUnit = 0
        self.mapMaxUnit = 0

        self.blockList = []
        self.useBlockNum = 0

    def getnormalizedscore(self):
        return self.score / self.useBlockNum

    def isslotpossible (self, row, column):
        return self.mapArray[row, column, 1]

    def popblockfromlist (self, block):
        for b in self.blockList:
            if b.level == block.level and b.type == block.type:
                self.blockList.remove (b)
                break

    def addblock (self, row, column, block):
        retq = []
        row += 4
        column += 4
        for i in range (5):
            for j in range (5):
                if block.map[i,j] == 0:
                    continue
                new_obj = copy.deepcopy (self)
                new_map = new_obj.mapArray[:,:,:]
                new_map_1 = new_map[row-i:row-i+5, column-j:column-j+5,1]
                new_map_2 = new_map[row-i:row-i+5, column-j:column-j+5,2]

                new_map_1 -= block.map

                # Check possibility
                possi = True
                new_score = 0
                for ii in range (5):
                    for jj in range (5):
                        if new_map_1[ii,jj] < 0:
                            possi = False
                        elif block.map[ii,jj] == 1 and new_map_1[ii,jj] == 0:
                            new_score += new_map_2[ii,jj]

                if possi == True:
                    new_obj.updatescore (new_obj.score + new_score)
                    new_obj.popblockfromlist (block)
                    new_obj.useBlockNum += (block.level + 1)
                    retq.append (new_obj)

        return retq

    def addfirstblock (self, row, column, block):
        retq = []
        row += 4
        column += 4
        
        new_obj = copy.deepcopy (self)
        new_map = new_obj.mapArray[:,:,:]
        new_map_1 = new_map[row-2:row+3, column-2:column+3,1]
        new_map_2 = new_map[row-2:row+3, column-2:column+3,2]

        new_map_1 -= block.map

        # Check possibility
        possi = True
        new_score = 0
        for ii in range (5):
            for jj in range (5):
                if new_map_1[ii,jj] < 0:
                    possi = False
                elif block.map[ii,jj] == 1 and new_map_1[ii,jj] == 0:
                    new_score += new_map_2[ii,jj]

        if possi == True:
            new_obj.updatescore (new_obj.score + new_score)
            new_obj.popblockfromlist (block)
            new_obj.useBlockNum += (block.level + 1)
            retq.append (new_obj)

        return retq


    def updatemap (self, new_map):
        self.mapArray = new_map
    def updatescore (self, score):
        self.score = score

    def initscore (self, s, score):
        for i in range (MainMap.MAX_HEIGHT + 8):
            for j in range (MainMap.MAX_WIDTH + 8):
                if self.mapArray[i,j,0] == s:
                    self.mapArray[i,j,2] = score

    def updateblocklist (self, blockList):
        self.blockList = copy.deepcopy (blockList)
                
    def printmap(self, e):
        emptyline = int ((MainMap.MAX_WIDTH - self.curWidth)/2) + 4

        print ("    ",end='')
        for i in range (emptyline, MainMap.MAX_WIDTH+8-emptyline):
            print ("%02d  "%(i - emptyline), end='')
        print ("")
        print ("    " + "----"*24)
        for i in range (emptyline, MainMap.MAX_HEIGHT+8-emptyline):
            print ("%02d| "%(i - emptyline),end='')
            for j in range (emptyline, MainMap.MAX_WIDTH+8-emptyline):
                print ("\033[0;%dm" %(30+self.mapArray[i,j,0]%8), end='')
                print ("%02d  " %(self.mapArray[i,j,e]), end='')
                print ("\033[0m", end='')
            print ("")

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
            self.curHeight = 20
        elif self.unionLev >= 10:
            self.curWidth = 20
            self.curHeight = 18
        elif self.unionLev >= 8:
            self.curWidth = 18
            self.curHeight = 16
        elif self.unionLev >= 6:
            self.curWidth = 16
            self.curHeight = 14
        elif self.unionLev >= 4:
            self.curWidth = 14
            self.curHeight = 12
        else:
            self.curWidth = 12
            self.curHeight = 10

        # Initialize Map
        emptyline = int ((MainMap.MAX_WIDTH - self.curWidth)/2) + 4
        for i in range (emptyline, MainMap.MAX_HEIGHT+8-emptyline):
            for j in range (emptyline, MainMap.MAX_WIDTH+8-emptyline):
                # Set current slot is possible
                self.mapArray[i,j,1] = 1
                # Set section of map
                if i >= j and i < (MainMap.MAX_HEIGHT+8-j) and i < 14 and j < 15:
                    self.mapArray[i,j,0] = 0
                    if j > 8:
                        self.mapArray[i,j,0] += 1
                elif i >= j-1 and i < (MainMap.MAX_HEIGHT+8-j) and i >= 14 and j < 15:
                    self.mapArray[i,j,0] = 2
                    if j > 8:
                        self.mapArray[i,j,0] += 1
                elif i >= j-1 and i >= (MainMap.MAX_HEIGHT+8-j) and i >= 14 and j < 15:
                    self.mapArray[i,j,0] = 4
                    if i < 19:
                        self.mapArray[i,j,0] += 1
                elif i >= j-1 and i >= (MainMap.MAX_HEIGHT+8+1-j) and i >= 14 and j >= 15:
                    self.mapArray[i,j,0] = 6
                    if i < 19:
                        self.mapArray[i,j,0] += 1
                elif i < j-1 and i >= (MainMap.MAX_HEIGHT+8+1-j) and i >= 14 and j >= 15:
                    self.mapArray[i,j,0] = 8
                    if j < 21:
                        self.mapArray[i,j,0] += 1
                elif i < j and i >= (MainMap.MAX_HEIGHT+8+1-j) and i < 14 and j >= 15:
                    self.mapArray[i,j,0] = 10
                    if j < 21:
                        self.mapArray[i,j,0] += 1
                elif i < j and i < (MainMap.MAX_HEIGHT+8+1-j) and i < 14 and j >= 15:
                    self.mapArray[i,j,0] = 12
                    if i > 8:
                        self.mapArray[i,j,0] += 1
                elif i < j and i < (MainMap.MAX_HEIGHT+8-j) and i < 14 and j < 15:
                    self.mapArray[i,j,0] = 14
                    if i > 8:
                        self.mapArray[i,j,0] += 1
                else:
                    print ("Couldn't be here i : %d j : %d" %(i,j))







            
