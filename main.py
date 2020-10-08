#!/usr/bin/python3
from map import MainMap

def main_start ():
    mainMap = MainMap ()
    total_score = mainMap.calcscore ()
    mainMap.initialize (5320)

if __name__ == "__main__":
    main_start ()
