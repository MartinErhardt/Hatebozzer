#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from bot import irc_bot
from script_parser import interpreter

def main():
    interpreter_main = interpreter("./scripts/hello_world.ht")
    interpreter_main.start()
    while 1:
        try:# still on Pyhon 2.X
            inp = raw_input(">")
        except NameError:# We are running on Python 3
            inp = input(">")
        interpreter_main.interprete_line(inp,0)
    sys.exit(0)
    
if __name__ == '__main__': main()
