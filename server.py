# Server object for tic-tac-toe
import tornado.ioloop
import tornado.web
import sys, os
from urllib.parse import urlparse
from tictactoe import TicTacToe

port = sys.argv[1]
checkpointRate = sys.argv[2]
databaseServer = sys.argv[3]
ttt = TicTacToe(3)
count = 0

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
	params = urllib.urlencode({'board': serializedBoard})
	conn = httplib.HTTPConnection(databaseServer)
	conn.request("GET", "/checkpoint?"+params)
	rsp = conn.getresponse()

def writeLog(move):
	params = urllib.urlencode({'move': move})
	conn = httplib.HTTPConnection(databaseServer)
	conn.request("GET", "/log?"+params)
	rsp = conn.getresponse()

def initState():
	global LOGFILE
	# If file exists, read latest checkpoint (aka last row)
	if (os.path.isfile(LOGFILE)):
		with open(LOGFILE, 'rb') as fh:
			recoveredBoard = fh.readlines()[-1].decode()
			deserial = deserializeBoard(recoveredBoard)
			print("recovered from: ", deserial)
			ttt.setBoard(deserial)

	else:
		# Otherwise, initialize new file with empty board
		lf = open(LOGFILE, "a+")
		emptyBoard = serializeBoard(ttt.newBoard())
		lf.write(emptyBoard)
		lf.close()

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

		print(query_components)
		row = query_components["row"]
		col = query_components["col"]
		player = query_components["player"]
		response = ttt.makeMove(int(row), int(col), player)
		status_resp = {"status" : response}
		print(status_resp)
		self.write(status_resp)

		# Log every move
		move = row + " " + col + " " + player + "\n"
		writeLog(move)

		board = ttt.getBoard()

		# Check if game is over, if so, write a new empty board 
		newBoard = None
		if (ttt.gameOver()):
			newBoard = ttt.newBoard()
		# Serialzie the original board
		serialized = serializeBoard(board)
		if count%checkPoint == 0:
			writeCheckpoint(serialized)
		
		if (newBoard):
			sb = serializeBoard(newBoard)
			writeCheckpoint(sb)

		checkpointfile.close()





class HeartbeatHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("ALIVE")

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
		(r"/heartbeat", HeartbeatHandler),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(port)
	tornado.ioloop.IOLoop.current().start()
