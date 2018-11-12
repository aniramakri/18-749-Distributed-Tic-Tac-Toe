# Server object for tic-tac-toe
import tornado.ioloop
import tornado.web
import sys
from urllib.parse import urlparse
from tictactoe import TicTacToe

port = sys.argv[1]
ttt = TicTacToe(3)


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


class MainHandler(tornado.web.RequestHandler):
	def get(self):
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
		logfile = open("log.txt", "a+")
		board = ttt.getBoard()
		serialized = serializeBoard(board)
		logfile.write(serialized)
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
