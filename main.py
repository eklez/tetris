#!/usr/bin/python3
from map import MainMap
from block import Block 

def main_start ():
    mainMap = MainMap ()
    mainMap.initialize (4720)
    new_block = Block (0, 4)
    ret = mainMap.addblock (10,10, new_block)
    for i in ret:
        mainMap.updatemap (i)
        mainMap.printmap (1)
        print ("")


if __name__ == "__main__":
    main_start ()
