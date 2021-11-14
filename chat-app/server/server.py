import socket
import threading






class Server:

	def __init__(self):

		self.setup_server()
		self.clients = []
		self.usernames = []
		self.server.listen()
		self.receive()


	def setup_server(self):
		try:
			self.host = socket.gethostbyname(socket.gethostname())
		except:
			print("Could not automatically find your local ip address")
			self.host = input("Please enter it manually: ")

		self.port = 9999

		try:
			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.bind((self.host,self.port))
		except:
			print("There was an error while setting up the server, please try again")
			quit()

		print(f"Running on HOST: {self.host}  PORT: {self.port}")


		

	def broadcast(self, message):
		for client in self.clients:
			client.send(message)


	def handle(self, client):
		self.send_users_list()
		while True:
			try:
				message = client.recv(1024)
				self.broadcast(message)

				if not message:
					index = self.clients.index(client)
					self.clients.remove(client)
					client.close()
					username = self.usernames[index]
					self.usernames.remove(username)
					self.send_users_list()
					break

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



if __name__ == "__main__":
	server1 = Server()
