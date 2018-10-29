### Client object for tic-tac-toe

import httplib
import sys

def makeMove(row, col):

http_server = sys.argv[1]
conn = httplib.HTTPConnection(http_server)

while 1:
	cmd = raw_input("Make your next move?")
	cmd = cmd.split()
	row, col = cmd[0], cmd[1]

	conn.request("POST", args)

	rsp = conn.getresponse()

	print(rsp.status, rsp.reason)
	data_received = rsp.read()
	print(data_received)

conn.close

