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

def attempt_connect(connect_http_server, params):
	attempt_start = time.time()
	global conn
	global current_http_server
	while(1):
		try:
			conn = httplib.HTTPConnection(connect_http_server)
			conn.request("GET", "/heartbeat?"+params)
			rsp = conn.getresponse()
			response = rsp.read()
			current_http_server = connect_http_server
			return True
		except Exception as e:
			if time.time() - attempt_start > 3 * heartbeatInterval:
				return False
			else:
				continue




def heartbeat():
	global conn
	global current_http_server
	global playerNum
	hbCount = 0
	while 1:
		params = urllib.urlencode({})
		try:
			conn.request("GET", "/heartbeat?"+params)
			rsp = conn.getresponse()
			response = rsp.read()
			print("# " + playerNum + " # " + response)
		except Exception as e:
			print("# " + playerNum + " # " + time.ctime() + ": " + current_http_server + " is not connecting")
			print(e)
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
			print("# " + playerNum + " # " + time.ctime() + ": " + current_http_server + " is officially down")
			if current_http_server == http_server_1:
				connect_http_server = http_server_2
			else:
				connect_http_server = http_server_1
			while 1:
				print("# " + playerNum + " # " + time.ctime() + ": " + "Attempting to connect to " +  connect_http_server )
				attempt = attempt_connect(connect_http_server, params)
				if attempt:
					hbCount = 0
					break
				else:
					if connect_http_server == http_server_1:
						connect_http_server = http_server_2
					else:
						connect_http_server = http_server_1

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
