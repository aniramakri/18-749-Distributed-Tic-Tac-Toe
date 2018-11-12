# Server object for tic-tac-toe
import tornado.ioloop
import tornado.web
import sys, os
from urllib.parse import urlparse
from tictactoe import TicTacToe

port = sys.argv[1]
ttt = TicTacToe(3)
LOGFILE = "log.txt"
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
		global LOGFILE
		global count

		if count == 0:
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

		# Checkpoint every move
		logfile = open(LOGFILE, "a+")
		board = ttt.getBoard()

		# Check if game is over, if so, write a new empty board 
		newBoard = None
		if (ttt.gameOver()):
			newBoard = ttt.newBoard()
		# Serialzie the original board
		serialized = serializeBoard(board)
		logfile.write(serialized)
		
		if (newBoard):
			sb = serializeBoard(newBoard)
			logfile.write(sb)

		logfile.close()




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
