#!/usr/bin/python3
from map import MainMap
from block import Block
import configparser

blockList = []
TOTAL_UNION = 0
THRESHOLD = 0.5
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

def check_duplicate (m, mlist):
    for i in mlist:
        comparison = i.mapArray[:,:,1] == m.mapArray[:,:,1]
        if comparison.all ():
            return True
    return False

def check_block_all (m, row, column, b):
    possible_ret = []
    for i in m.addblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()

    b.flip ()
    for i in m.addblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter () 
    for i in m.addblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    b.flip ()

    return possible_ret


def main_start ():

    # Initialize
    if readconf () == False:
        return False
    mainMap = MainMap ()
    mainMap.initialize (TOTAL_UNION)
    mainMap.updateblocklist (blockList)
    initialize_score (mainMap)

    global THRESHOLD
    max_n_score = 0
    level_list = []
    depth_list = []

    # No level_list : level_list == mainMap
    # First place to put block
    first = [9, 10]
    for b in mainMap.blockList:
        ret = check_block_all (mainMap, first[0], first[1], b)
        for e in ret:
            normalized_score = e.getnormalizedscore ()
            if normalized_score > max_n_score:
                if max_n_score < normalized_score - THRESHOLD:
                    depth_list.clear ()
                max_n_score = normalized_score
                depth_list.append (e)
            elif normalized_score == max_n_score:
                depth_list.append (e)
            else:
                continue

    print ("First Round End")
    level_list = depth_list
    depth_list = []
    second = [9,7]
    for e in level_list:
        for b in e.blockList:
            ret = check_block_all (e, second[0], second[1], b)
            for bb in ret:
                normalized_score = bb.getnormalizedscore ()
                if normalized_score > max_n_score:
                    if max_n_score < normalized_score - THRESHOLD:
                        depth_list.clear ()
                    max_n_score = normalized_score
                    depth_list.append (bb)
                elif normalized_score == max_n_score:
                    depth_list.append (bb)
                else:
                    continue

    for e in depth_list:
        e.printmap(1)

if __name__ == "__main__":
    main_start ()
