### Client object for tic-tac-toe

import httplib, urllib
import sys

http_server = sys.argv[1]
playerNum = sys.argv[2]
conn = httplib.HTTPConnection(http_server)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


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

