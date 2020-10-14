#!/usr/bin/python3
import numpy as np

# Block
#
# Level 0 : 1 block
# Level 1 : 2 block
# Level 2 : 3 block
# Level 3 : 4 block
# Level 4 : 5 block
#
# type 0 ~ 4 : class
#
# map : 5x5 bitmap
class Block:
    # Initialize function
    def init_type1 (self, level):
        self.map[2,2] = 1
        if level < 1: return
        self.map[2,3] = 1
        if level < 2: return
        self.map[3,2] = 1
        if level < 3: return
        self.map[3,3] = 1
        if level < 4: return 
        self.map[2,4] = 1
    def init_type2 (self, level):
        self.map[2,2] = 1
        if level < 1: return
        self.map[2,3] = 1
        if level < 2: return
        self.map[2,1] = 1
        if level < 3: return
        self.map[3,2] = 1
        if level < 4: return 
        self.map[1,2] = 1
    def init_type3 (self, level):
        self.map[2,2] = 1
        if level < 1: return
        self.map[2,3] = 1
        if level < 2: return
        self.map[2,1] = 1
        if level < 3: return
        self.map[2,4] = 1
        if level < 4: return 
        self.map[2,0] = 1
    def init_type4 (self, level):
        self.map[2,2] = 1
        if level < 1: return
        self.map[2,3] = 1
        if level < 2: return
        self.map[2,1] = 1
        if level < 3: return
        self.map[3,3] = 1
        if level < 4: return 
        self.map[1,3] = 1
    def init_type5 (self, level):
        self.map[2,2] = 1
        if level < 1: return
        self.map[2,3] = 1
        if level < 2: return
        self.map[3,2] = 1
        if level < 3: return
        self.map[1,3] = 1
        if level < 4: return 
        self.map[0,3] = 1

    def __init__(self, blocktype, level):
        self.level = level
        self.type = blocktype
        self.map = np.zeros ([5, 5])

        if blocktype == 0:
            self.init_type1(level)
        elif blocktype == 1:
            self.init_type2(level)
        elif blocktype == 2:
            self.init_type3(level)
        elif blocktype == 3:
            self.init_type4(level)
        elif blocktype == 4:
            self.init_type5(level)

    def rotate_counter (self):
        self.map = np.rot90 (self.map)
    def flip (self):
        self.map = np.flip (self.map, 0)

