For running server: python3 server.py 8888 1 localhost:9000 ALICE
					(server port) (checkpointing rate) (database localhost)
For running database: python3 database.py 9000
					 (port number)
For running client: python2 client.py localhost:8888 localhost:9999 p1 2

                                        (server1)(server2)(player)(heartbeat)
