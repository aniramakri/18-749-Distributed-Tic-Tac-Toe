# Server object for tic-tac-toe
import tornado.ioloop
import tornado.web
import sys, os
from urllib.parse import urlparse,unquote
from tictactoe import TicTacToe
import http.client, urllib

def serializeBoard(board):
    serialized = ""
    for elt in board:
        serialized += str(elt) + ","

    serialized += "\n"
    return serialized

def deserializeBoard(s):
    delimiter = ","
    board = []

    for c in s:
        if (c == delimiter) or (c == '\n'):
            pass
        else:
            board.append(c)

    return board

def writeCheckpoint(serializedBoard):
	params = urllib.parse.urlencode({'board': serializedBoard.encode()})
	conn = http.client.HTTPConnection(databaseServer)
	conn.request("GET", "/checkpoint?"+params)
	rsp = conn.getresponse()

def writeLog(move):
	params = urllib.parse.urlencode({'log': move})
	conn = http.client.HTTPConnection(databaseServer)
	conn.request("GET", "/log?"+params)

def getLog():
	params = urllib.parse.urlencode({'move': " "})
	conn = http.client.HTTPConnection(databaseServer)
	conn.request("GET", "/grabLog?"+params)
	rsp = conn.getresponse()
	return rsp.read().decode('utf-8')

def getCheckpoint():
	params = urllib.parse.urlencode({'state': " "})
	conn = http.client.HTTPConnection(databaseServer)
	conn.request("GET", "/grabCheckpoint?"+params)
	rsp = conn.getresponse()
	return rsp.read().decode('utf-8')


def initState():
	recoveredBoard = getCheckpoint()
	deserial = deserializeBoard(recoveredBoard)
	print("Recovered from: ", deserial)
	ttt.setBoard(deserial)
	print("Replaying the following missed moves")
	logs = getLog()
	print(logs)
	totalLogs = logs.split("\n")
	for log in totalLogs:
		args = log.split(" ")
		if len(args) == 3:
			response = ttt.makeMove(int(args[0]), int(args[1]), args[2], False, False)
			status_resp = {"status" : response}


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		global CHECKPOINTFILE
		global LOGFILE
		global count
		global checkpointRate

		if count == 0:
			print("initializing state")
			initState()

		count += 1

		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))
		row = query_components["row"]
		col = query_components["col"]
		player = query_components["player"]
		response = ttt.makeMove(int(row), int(col), player)
		status_resp = {"status" : response}
		self.write(status_resp)

		# Log every move
		move = row + " " + col + " " + player + "\n"
		writeLog(move)

		board = ttt.getBoard()

		# Check if game is over, if so, write a new empty board
		if (ttt.gameOver()):
			print("NEW GAME :)")
			newBoard = ttt.newBoard()
			ttt.setBoard(newBoard)
			ttt.drawBoard()
			sb = serializeBoard(newBoard)
			writeCheckpoint(sb)
		else:
			# Serialzie the original board
			serialized = serializeBoard(board)
			if count%checkpointRate == 0:
				writeCheckpoint(serialized)

class HeartbeatHandler(tornado.web.RequestHandler):
	def get(self):
		global serverName
		self.write(serverName)
		self.write(" IS ALIVE")

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
		(r"/heartbeat", HeartbeatHandler),
	])

port = sys.argv[1]
checkpointRate = int(sys.argv[2])
databaseServer = sys.argv[3]
serverName = sys.argv[4]
ttt = TicTacToe(3)
ttt.drawBoard()
count = 0


if __name__ == "__main__":

	app = make_app()
	app.listen(port)
	tornado.ioloop.IOLoop.current().start()
