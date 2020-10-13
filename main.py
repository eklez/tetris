#!/usr/bin/python3
from map import MainMap
from block import Block
import configparser

blockList = []
TOTAL_UNION = 0
config = configparser.ConfigParser ()

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
    global config
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

def initialize_score (m):
    global config

    for i in range (16):
        score = int (config['SECTION_SCORE']['SEC'+str(i)])
        m.initscore (i, score)

def main_start ():

    # Initialize
    if readconf () == False:
        return False
    mainMap = MainMap ()
    mainMap.initialize (TOTAL_UNION)
    mainMap.updateblocklist (blockList)
    initialize_score (mainMap)

    mainMap.printmap (2)
    ret = mainMap.addblock (10,10,mainMap.blockList[0])
    for i in ret:
        print (i.score)
        i.printmap (1)

if __name__ == "__main__":
    main_start ()
