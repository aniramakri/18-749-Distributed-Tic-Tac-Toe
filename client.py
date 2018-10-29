### Client object for tic-tac-toe

import httplib, urllib
import sys

def makeMove(row, col):

http_server = sys.argv[1]
playerNum = sys.argv[2]
conn = httplib.HTTPConnection(http_server)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


while 1:
	cmd = raw_input("Make your next move?")
	cmd = cmd.split()
	row, col = cmd[0], cmd[1]
	params = urllib.urlencode({'@player': playerNum, '@row': row, '@col': col})

	conn.request("POST", "", params, headers)
	rsp = conn.getresponse()
	response = rsp.read()

	if response == 'INVALID MOVE':
		cmd = print("Invalid Move! Try again!")
		continue
	else:
		print(response)
		print("Waiting for other player to make a move!")
		conn.request("GET", "/")

		rsp = conn.getresponse()
		response = rsp.read()
		print("Other player moved!")
		print(response)

conn.close

