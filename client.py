### Client object for tic-tac-toe

import httplib, urllib
import sys, time, thread

http_server = sys.argv[1]
playerNum = sys.argv[2]
# In seconds
heartbeatInterval = sys.argv[3]
conn = httplib.HTTPConnection(http_server)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


def move():
    while 1:
    	cmd = raw_input("Make your next move?")
    	cmd = cmd.split()
    	row, col = cmd[0], cmd[1]
    	params = urllib.urlencode({'player': playerNum, 'row': row, 'col': col})

    	conn.request("GET", "/?"+params)
    	rsp = conn.getresponse()
    	response = rsp.read()
    	print(response)

    conn.close


def heartbeat():
	pass


try:
	print("In try")
	thread.start_new_thread(move, ())
except:
	print("Error, unable to start new thread")
while 1:
	pass
