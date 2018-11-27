# Server object for tic-tac-toe
import tornado.ioloop
import tornado.web
import sys, os
from urllib.parse import urlparse, unquote
from tictactoe import TicTacToe

port = sys.argv[1]
CHECKPOINTFILE = "checkpoint.txt"
LOGFILE = "log.txt"

class LogHandler(tornado.web.RequestHandler):
	def get(self):
		global CHECKPOINTFILE
		global LOGFILE
		global count
		global checkpointRate

		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))

		log = unquote(query_components["log"]).replace('+', ' ')
		print(log)
		# Checkpoint every move
		logFile = open(LOGFILE, "a+")
		logFile.write(log)
		logFile.close()


class CheckpointHandler(tornado.web.RequestHandler):
	def get(self):
		global CHECKPOINTFILE
		global LOGFILE
		print("ADDING CHECKPOINT")
		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))

		state = unquote(query_components["board"]).replace('+', ' ')
		print(state)
		# Checkpoint every move
		checkpointfile = open(CHECKPOINTFILE, "a+")
		checkpointfile.write(state)
		checkpointfile.close()

		# Clear log file
		open(LOGFILE, "w").close()

class GrabCheckpointHandler(tornado.web.RequestHandler):
	def get(self):
		print("GRABBING CHECKPOINT")
		global CHECKPOINTFILE
		# Grab latest checkpoint
		with open(CHECKPOINTFILE, 'rb') as fh:
			recoveredBoard = fh.readlines()[-1].decode()

		self.write(recoveredBoard)

class GrabLogHandler(tornado.web.RequestHandler):
	def get(self):
		print("GRABBING LOG")
		global CHECKPOINTFILE
		global LOGFILE
		# Checkpoint every move
		with open(LOGFILE, 'rb') as fh:
			moves = fh.read()
		self.write(moves)


def make_app():
	return tornado.web.Application([
		(r"/checkpoint", CheckpointHandler),
		(r"/log", LogHandler),
		(r"/grabCheckpoint", GrabCheckpointHandler),
		(r"/grabLog", GrabLogHandler)
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(port)
	tornado.ioloop.IOLoop.current().start()
