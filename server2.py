import socket
import threading


HOST = '192.168.1.106'
PORT = 9998



class Server:

	def __init__(self, host, post):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clients = []
		self.usernames = []
		self.server.bind((HOST,PORT))
		self.server.listen()


	def broadcast(self, message):
		for client in self.clients:
			client.send(message)


	def handle(self, client):
		self.send_users_list()
		while True:
			try:
				message = client.recv(1024)
				self.broadcast(message)

			except:
				index = self.clients.index(client)
				self.clients.remove(client)
				client.close()
				username = self.usernames[index]
				self.usernames.remove(username)
				self.send_users_list()
				break


	def receive(self):
		while True:
			client, address = self.server.accept()
			print("Connected with {}".format(str(address)))

			username = client.recv(1024).decode('ascii')
			self.usernames.append(username)
			self.clients.append(client)

			print("Username is {}".format(username))

			thread = threading.Thread(target=self.handle, args=(client,))
			thread.start()
			

	def send_users_list(self):
		message = "<users>" + '\n'.join(self.usernames)
		message = message.encode("ascii")
		self.broadcast(message)




server1 = Server(HOST, PORT)
server1.receive()