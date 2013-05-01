#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from bot import bot
def main():
    bot_main= bot( "irc.freenode.net",6667,"botty botty botty :Python IRC","hello_nick","#martin3333" )
    bot_main.start()
    while 1:
        try:
            inp = raw_input()
        except NameError:
            inp = input()
        if inp =="!QUIT": 
            bot_main.stop()
            break
    sys.exit(0)
    
if __name__ == '__main__': main()
