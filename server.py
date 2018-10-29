# Server object for tic-tac-toe
import tornado.ioloop
import tornado.web
import sys
from urllib.parse import urlparse
from tictactoe import TicTacToe

port = sys.argv[1]
ttt = TicTacToe(3)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		print("Hello")
		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))
		logfile = open("log.txt", "a+")
		logfile.write(str(query_components))
		logfile.write("\n")
		logfile.close()
		print(query_components)
		row = query_components["row"]
		col = query_components["col"]
		player = query_components["player"]
		response = ttt.makeMove(int(row), int(col), player)
		status_resp = {"status" : response}
		print(status_resp)
		self.write(status_resp)

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(port)
	tornado.ioloop.IOLoop.current().start()
