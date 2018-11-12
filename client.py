### Client object for tic-tac-toe

import httplib, urllib
import sys, time, thread

http_server_1 = sys.argv[1]
http_server_2 = sys.argv[2]
playerNum = sys.argv[3]
current_http_server = http_server_1
# In seconds
heartbeatInterval = float(int(sys.argv[4]))
conn = httplib.HTTPConnection(current_http_server)
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


def move():
    while 1:
    	cmd = raw_input("Make your next move?")
    	cmd = cmd.split()
    	row, col = cmd[0], cmd[1]
    	params = urllib.urlencode({'player': playerNum, 'row': row, 'col': col})

    	conn.request("GET", "/?"+params)
    	rsp = conn.getresponse()
    	response = rsp.read()
    	print(response)

    conn.close


def heartbeat():
	global conn
	global current_http_server
	hbCount = 0
	while 1:
		params = urllib.urlencode({})
		try:
			conn.request("GET", "/heartbeat?"+params)
			rsp = conn.getresponse()
			response = rsp.read()
			print(response)
		except:
			print("Down")
			try:
				conn = httplib.HTTPConnection(current_http_server)
				conn.request("GET", "/heartbeat?"+params)
				rsp = conn.getresponse()
				response = rsp.read()
			except:
				pass

			if hbCount != 3:
				hbCount += 1

		if hbCount == 3:
			print("Actually down")
			while 1:
				try:
					if current_http_server == http_server_1:
						connect_http_server = http_server_2
					else:
						connect_http_server = http_server_1
					conn = httplib.HTTPConnection(connect_http_server)
					conn.request("GET", "/heartbeat?"+params)
					rsp = conn.getresponse()
					response = rsp.read()
					hbCount = 0
					current_http_server = connect_http_server
					break
				except Exception as e:
					#print(e)
					#time.sleep(heartbeatInterval)
					continue

		# Sleep for the amount of time to simualte heartbeat
		time.sleep(heartbeatInterval)


try:
	print("In try")
	thread.start_new_thread(move, ())
	thread.start_new_thread(heartbeat, ())
except:
	print("Error, unable to start new thread")
while 1:
	pass
