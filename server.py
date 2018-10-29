# Server object for tic-tac-toe
#import os, math
#import http.server
#import socketserver
import tornado.ioloop
import tornado.web
import sys
from urllib.parse import urlparse

port = sys.argv[1]

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		query = urlparse(self.request.uri).query
		query_components = dict(qc.split("=") for qc in query.split("&"))
		print(query_components)
		row = query_components["row"]
		col = query_components["col"]
		player = query_components["player"]

def make_app():
	return tornado.web.Application([
		(r"/", MainHandler),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(port)
	tornado.ioloop.IOLoop.current().start()
