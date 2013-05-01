import socket
import random
import os
import threading

class bot(threading.Thread):
   def __init__( self, net, port, user, nick, start_chan ): 
       self.id= random.randint(0,1000)
       self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
       self.irc_connect ( net, port )
       self.irc_set_user( user,nick )
       self.irc_join( start_chan )
       self.finnish=False
       threading.Thread.__init__(self)
       
   def run( self ):
       while not self.finnish:
           serv_data_rec = (self.irc.recv ( 4096 )).decode("utf-8")
           if serv_data_rec.find ( "PING" ) != -1:
               self.irc.send( ("PONG"+ serv_data_rec.split() [ 1 ] + "\r\n").encode("utf-8") )
               
           elif serv_data_rec.find("PRIVMSG")!= -1:
               line = serv_data_rec.split( "!" ) [ 0 ] + " :" + serv_data_rec.split( ":" ) [ 2 ]
               
               self.irc_log( line )
               self.irc_message( line )
   
   def stop( self ):
       self.finnish = True
       self.irc_quit()
       
   def irc_connect( self, net, port ):
       self.net = net
       self.port = port
       self.irc.connect ( ( net, port ) )
   
   def irc_set_user( self, user, nick ):
       self.user = user
       self.nick = nick
       self.irc.send( ("NICK " + nick + "\r\n")					.encode("utf-8") )
       self.irc.send( ("USER " + user + "\r\n")					.encode("utf-8") )
   
   def irc_join( self, chan ):
       self.chan = chan
       self.irc.send( ("JOIN " + chan + "\r\n")					.encode("utf-8") )
   
   def irc_message( self, msg ):
       self.irc.send( ("PRIVMSG " + self.chan+" " + msg + " \r\n")			.encode('utf-8') )
   
   def irc_message_nick( self, msg , nick):
       self.irc.send( ("PRIVMSG " + self.chan+" " + nick + " " + msg + " \r\n")	.encode('utf-8') )
       
   def irc_ping( self ):
       self.irc.send( ("PING :" + self.net)						.encode("utf-8") )
       
   def irc_log( self, line ):
       if not os.path.exists("./logs"):
           os.makedirs("./logs")
       f = open("./logs/" + self.net + self.chan + "#" + "% s" % self.id,'a')
       try:
           f.write( line )
       finally:
           f.close()
   
   def irc_quit( self ):
       self.irc.send( ("QUIT\r\n")							.encode("utf-8") )
   
   def irc_quit_msg(self, msg):
       self.irc.send( ("QUIT :" + msg + "\r\n")					.encode("utf-8") )

