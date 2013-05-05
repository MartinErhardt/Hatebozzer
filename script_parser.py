#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import threading, thread
import sys
import asyncore
from bot import irc_bot
import bot
#import hatebozzer

class interpreter(threading.Thread):
    def __init__( self, path): 
        try:
            f = open(path,'r')
            self.script_lines=f.read().split("\n")
        finally:
            f.close()
        self.bot_n=0
        self.cur_index=0
        self.path=path
        self.var_names=[]
        self.var_val=[]
        self.builtin_func=("/connect","/nick","/user","/join","/say","/print","/quit")
        threading.Thread.__init__( self )
    
    def run(self):
        for cur_line in self.script_lines:
            self.interprete_line(cur_line,1)
            self.cur_index +=1
    
    def interprete_line( self, line, session_type):
        line = line.split("##")[0]# comments don't count
        if "=" in line:
            if "==" in line:
                pass
            else:
                var_name = line.split("=")[0]
                val      = line.split("=")[1]
                if var_name in self.var_names:
                    self.var_val[get_var_index(var_name)]=val
                else:
                    self.var_names.append(var_name)
                    self.var_val.append(val)
        if line.startswith("/"):
            func_name = "".join(line.split()).split("(")[0]
            arg_list  = self.parse_list(line, session_type )
            self.func( func_name, arg_list, session_type )
    
    def parse_list( self, line, session_type):
        if not line.strip().endswith(")"):
            self.err("SyntaxError", "Didn't closed list with \")\"",session_type)
        try:
            new_list  = line.split("(")[1].strip().strip(')').split(",")
        except IndexError:
            self.err("InternalIndexError","",session_type)
            sys.exit(-1)
        j=0
        for lookup_var in new_list:
            if lookup_var in self.var_names:
                new_list[j]=self.get_var(lookup_var)
            j=j+1
        return new_list
    
    def get_var(self,name):
        return self.var_val[self.get_var_index(name)]
    
    def get_var_index(self, name):
        return self.var_names.index(name)
    
    def func( self, name, arg_list, session_type):
        if name in self.builtin_func:
            try:
                if name == "/connect":
                    thread.start_new_thread(bot.bot_thread_entry,(arg_list[0],6667,arg_list[1],arg_list[2],arg_list[3],) )
                    success=False
                    while not success:
                        try:
                            self.bot=bot.bots[self.bot_n]
                            self.bot_n+=1
                            success=True
                        except IndexError:
                            continue
                elif name == "/nick":
                    self.bot.irc_set_nick( arg_list[0] )
                elif name == "/user":
                    self.bot.irc_set_user( arg_list[0] )
                elif name == "/join":
                    self.bot.irc_join( arg_list[0] )
                elif name == "/say":
                    self.bot.irc_message( ":"+arg_list[0],arg_list[1])
                elif name == "/print":
                    print ( arg_list[0] )
                elif name == "/quit":
                    self.bot.close()
                    sys.exit(0)
                else:
                    self.err( "SyntaxError", "Didn't found not builtin function: " + name, session_type )
            except IndexError:
                self.err("IndexError","too less arguments for builtin function",session_type )
        else:
            self.err("SyntaxError", "Didn't found not builtin function: " + name, session_type)
    def err( self, err_type, info, session_type ):
        if session_type == 1:
            print("\nHate Script: "+err_type+" ocurred\n"
              +info+"\n" 
              +"in file "+self.path+" in line: "+str(self.cur_index+1)+"\n"
              +str(self.script_lines[self.cur_index]))
        elif session_type == 0:
            print("\nHate Script: "+err_type+" ocurred\n"
              +info+"\n")
