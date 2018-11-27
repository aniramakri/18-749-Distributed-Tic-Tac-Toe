# Server object for tic-tac-toe
import tornado.ioloop
import tornado.web
import sys, os
from urllib.parse import urlparse
from tictactoe import TicTacToe

CHECKPOINTFILE = "checkpoint.txt"
LOGFILE = "log.txt"

class LogHandler(tornado.web.RequestHandler):
	def get(self):
		global CHECKPOINTFILE
		global LOGFILE
				global CHECKPOINTFILE
		global LOGFILE
		global count
		global checkpointRate

		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))

		log = query_components["log"]

		# Checkpoint every move
		logFile = open(LOGFILE, "a+")
		logFile.write(log)
		logFile.close()


class CheckpointHandler(tornado.web.RequestHandler):
	def get(self):
		global CHECKPOINTFILE
		global LOGFILE

		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))

		state = query_components["state"]

		status_resp = {"status" : response}
		print(status_resp)
		self.write(status_resp)

		# Checkpoint every move
		checkpointfile = open(CHECKPOINTFILE, "a+")
		checkpointfile.write(state)
		checkpointfile.close()

		# Clear log file
		open(LOGFILE, "w").close()

class GrabCheckpointHandler(tornado.web.RequestHandler):
	def get(self):
		global CHECKPOINTFILE

		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))

		state = query_components["state"]

		# Grab latest checkpoint
		with open(CHECKPOINTFILE, 'rb') as fh:
			recoveredBoard = fh.readlines()[-1].decode()

		status_resp = {"board" : recoveredBoard}
		self.write(status_resp)

class GrabLogHandler(tornado.web.RequestHandler):
	def get(self):
		global CHECKPOINTFILE
		global LOGFILE

		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))

		state = query_components["state"]

		# Checkpoint every move
		with open(LOGFILE, 'rb') as fh:
			moves = fh.readlines()
		status_resp = {"move" : moves}
		self.write(status_resp)


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
