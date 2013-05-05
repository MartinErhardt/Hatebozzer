#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, asyncore
import random
import os
import threading
import datetime

global bots
bots=[]

def bot_thread_entry(net, port, user, nick, start_chan):
    bot=irc_bot(net, port, user, nick, start_chan)
    bots.append(bot)
    asyncore.loop()

class irc_bot(asyncore.dispatcher):
   def __init__( self, net, port, user, nick, start_chan ): 
       asyncore.dispatcher.__init__(self)
       self.id= random.randint(0,1000)
       self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
       self.send_buf=""
       self.chan=[]
       self.send_Lock=threading.Lock()
       self.irc_connect ( net, port )
       self.irc_set_user( user )
       self.irc_set_nick( nick )
       self.irc_join( start_chan )


   def handle_connect(self):
       pass

   def handle_read(self):
       try:
            serv_data_rec = (self.recv ( 4096 )).decode("utf-8")
       except Exception as e:
            serv_data_rec=""
            print(e)
       if serv_data_rec.find ( "PING" ) != -1:
            self.irc_send( "PONG "+ serv_data_rec.split() [ 1 ] )
       elif serv_data_rec.find("PRIVMSG")!= -1:
            lines =serv_data_rec.split( ":" )
            chan= lines[1].split("PRIVMSG")[1]
            
            del lines[0:2]
            
            line = serv_data_rec.split( "!" ) [ 0 ] + " :" + "".join(lines)
            self.irc_log( line,chan)
            self.irc_message( line, chan )
   
   def handle_write(self):
       self.send((self.send_buf).encode("utf-8"))
       self.send_buf=""
   
   def handle_close(self):
       self.close()
       
   def irc_connect( self, net, port ):
       self.net = net
       self.port = port
       self.connect ( ( net, port ) )
   
   def irc_send( self, to_send ):
       self.send_Lock.acquire()
       self.send_buf=self.send_buf+to_send+"\r\n"
       self.send_Lock.release()
   
   def irc_set_nick( self, nick ):
       self.nick = nick
       self.irc_send("NICK " + nick)
   
   def irc_set_user( self, user):
       self.user = user
       self.irc_send( "USER " + user )
   
   def irc_join( self, chan ):
       self.chan.append(chan)
       self.irc_send( "JOIN " + chan )
   
   def irc_part( self, chan ):
       self.chan.remove(chan)
       self.irc_send( "PART " + chan )
   
   def irc_message( self, msg ,chan):
       self.irc_send( "PRIVMSG " + chan + " " + msg )
   
   def irc_message_nick( self, msg , nick, chan):
       self.irc_send("PRIVMSG " + chan+" " + nick + " " + msg )
   
   def irc_ping( self ):
       self.irc_send( "PING :" + self.net )
       
   def irc_log( self, line, chan):
       now = datetime.datetime.now()
       if not os.path.exists("./logs"):
           os.makedirs("./logs")
       try:
           f = open("./logs/" + self.net + chan + "#" + "% s" % self.id,'a')
           date=str(now.hour)+":"+str(now.minute)+":"+str(now.second)
           f.write( date+line )
           f.close()
       except Exception as e:
           print(e)
   
   def irc_quit( self ):
       self.irc_send( "QUIT" )
   
   def irc_quit_msg(self, msg):
       self.irc_send( "QUIT :" + msg )
