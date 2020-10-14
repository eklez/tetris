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
        if comparison.all () and i.useBlockNum == m.useBlockNum:
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

# Use only in first touch
def check_block_all_first (m, row, column, b):
    possible_ret = []
    for i in m.addfirstblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addfirstblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addfirstblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addfirstblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()

    b.flip ()
    for i in m.addfirstblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addfirstblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter () 
    for i in m.addfirstblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    for i in m.addfirstblock (row, column, b):
        if not check_duplicate (i, possible_ret):
            possible_ret.append (i)
    b.rotate_counter ()
    b.flip ()

    return possible_ret

def find_pos (m):
    ret_list = []
    emptyline = int ((m.MAX_WIDTH- m.curWidth)/2) + 4
    for i in range (emptyline, m.MAX_HEIGHT+8-emptyline):
        for j in range (emptyline, m.MAX_WIDTH+8-emptyline):
            if m.mapArray[i,j,1] == 0:
                continue
            # Boundary
            if (i == emptyline\
                or i == m.MAX_HEIGHT+8-emptyline-1\
                or j == emptyline\
                or j == m.MAX_WIDTH+8-emptyline-1):
                if i == emptyline and m.mapArray[i+1,j,1] == 0:
                    ret_list.append ([i,j])
                elif i == m.MAX_HEIGHT+8-emptyline -1 and m.mapArray[i-1,j,1] == 0:
                    ret_list.append ([i,j])
                elif j == emptyline and m.mapArray[i,j+1,1] == 0:
                    ret_list.append ([i,j])
                elif j == m.MAX_WIDTH+8-emptyline-1 and m.mapArray[i,j-1,1] == 0:
                    ret_list.append ([i,j])
            else:
                if (m.mapArray[i+1,j,1] == 0\
                    or m.mapArray[i-1,j,1] == 0\
                    or m.mapArray[i,j-1,1] == 0\
                    or m.mapArray[i,j+1,1] == 0):
                    ret_list.append ([i,j])

    return ret_list

def find_max_pos (m):
    ret_list = []
    possible_pos = find_pos (m)
    max_score = 0
    for e in possible_pos:
        tmpscore = m.mapArray[e[0],e[1],2]
        if tmpscore > max_score:
            max_score = tmpscore
            ret_list.clear ()
            ret_list.append (e)
        elif tmpscore == max_score:
            ret_list.append (e)
    return ret_list

def level_search (level_list):
    max_n_score = 0
    depth_list = []
    # Possible Map
    for eMap in level_list:
        pos_list = find_max_pos (eMap)
        # Possible Pos
        for ePos in pos_list:
            # Possible Block
            for eb in eMap.blockList:
                ret = check_block_all (eMap, ePos[0]-4, ePos[1]-4, eb)
                for e in ret:
                    normalized_score = e.getnormalizedscore ()
                    if normalized_score > max_n_score:
                        if max_n_score < normalized_score - THRESHOLD:
                            depth_list.clear ()
                        max_n_score = normalized_score
                        if not check_duplicate (e, depth_list):
                            depth_list.append (e)
                    elif normalized_score == max_n_score:
                        if not check_duplicate (e, depth_list):
                            depth_list.append (e)
                   
    return depth_list

def main_start ():

    # Initialize
    if readconf () == False:
        return False
    mainMap = MainMap ()
    mainMap.initialize (TOTAL_UNION)
    mainMap.updateblocklist (blockList)
    initialize_score (mainMap)

    global THRESHOLD
    level_list = []
    depth_list = []

    # No level_list : level_list == mainMap
    # First place to put block
    max_n_score = 0
    first = [9, 10]
    for b in mainMap.blockList:
        ret = check_block_all_first (mainMap, first[0], first[1], b)
        for e in ret:
            normalized_score = e.getnormalizedscore ()
            if normalized_score > max_n_score:
                if max_n_score < normalized_score - THRESHOLD:
                    depth_list.clear ()
                max_n_score = normalized_score
                if not check_duplicate (e, depth_list):
                    depth_list.append (e)
            elif normalized_score == max_n_score:
                if not check_duplicate (e, depth_list):
                    depth_list.append (e)
            else:
                continue

    print ("[+] First Round End")
    print ("[+] Total number of cases : %d" %(len (depth_list)))

    depth_list = level_search (depth_list)

    print ("[+] Second Round End")
    print ("[+] Total number of cases : %d" %(len (depth_list)))

    depth_list = level_search (depth_list)
    print ("[+] Third Round End")
    print ("[+] Total number of cases : %d" %(len (depth_list)))

    '''
    depth_list = level_search (depth_list)
    print ("[+] Fourth Round End")
    print ("[+] Total number of cases : %d" %(len (depth_list)))

    depth_list = level_search (depth_list)
    print ("[+] Fifth Round End")
    print ("[+] Total number of cases : %d" %(len (depth_list)))
    '''
    for e in depth_list:
        e.printmap (1)

if __name__ == "__main__":
    main_start ()
