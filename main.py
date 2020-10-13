#!/usr/bin/python3
from map import MainMap
from block import Block
import configparser

blockList = []
TOTAL_UNION = 0

def genblock (c, l):
    return Block (c, l)

def genblockclass (c, s):
    global blockList
    level = 0
    for i in s:
        for j in range (int (s[i])):
            new_block = genblock (c, level)
            blockList.append (new_block)
        level += 1


def readconf ():
    config = configparser.ConfigParser ()
    config.read ('config.ini')
    if not 'UNION_LEV' in config.sections ():
        print ("UNION_LEV in config.ini")
        return False

    global TOTAL_UNION 
    TOTAL_UNION = int (config['UNION_LEV']['LEV'])

    classzero = config['CLASS_0']
    classone = config['CLASS_1']
    classtwo = config['CLASS_2']
    classthree = config['CLASS_3']
    classfour = config['CLASS_4']

    genblockclass (0, classzero)
    genblockclass (1, classone)
    genblockclass (2, classtwo)
    genblockclass (3, classthree)
    genblockclass (4, classfour)

def main_start ():

    # Initialize
    if readconf () == False:
        return False
    mainMap = MainMap ()
    mainMap.initialize (TOTAL_UNION)

    print (len (blockList))

if __name__ == "__main__":
    main_start ()
