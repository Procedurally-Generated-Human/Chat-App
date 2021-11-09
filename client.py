import socket
import threading
import tkinter as tk
import tkinter.simpledialog as simpledialog

HOST = '192.168.1.106'
PORT = 9998

class Client:

	def __init__(self, host, port):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((host, port))
		self.get_and_send_username()
		self.create_main_window() 
		
		

	def get_and_send_username(self):
		self.dialog_window = tk.Tk()
		self.dialog_window.withdraw()
		self.username = simpledialog.askstring("Welcome","Please Choose a Username", parent=self.dialog_window)
		self.client_socket.send(self.username.encode('ascii'))



	def create_main_window(self):
		# create window
		self.main_window = tk.Tk()
		self.main_window.title("Global Chatroom")
		self.main_window.geometry('700x440')
		self.main_window.resizable(False, False)

		# chat area and users list
		self.chat_and_username_frame = tk.Frame(self.main_window)
		self.chat_area = tk.Text(self.chat_and_username_frame, height=25, width=65, font=("Courier", 15))
		self.chat_area.bind("<Key>", lambda e: "break") # prevents user from changing text area
		self.chat_area.pack(side = tk.LEFT)
		self.username_area = tk.Text(self.chat_and_username_frame, height=25, width=17, font=("Courier", 15))
		self.username_area.bind("<Key>", lambda e: "break")
		self.username_area.pack(side = tk.RIGHT)

		# send message input area and button
		self.send_area_frame = tk.Frame(self.main_window)
		self.send_area = tk.Entry(self.send_area_frame, width=57)
		self.send_area.pack(side=tk.LEFT)
		self.send_button = tk.Button(self.send_area_frame, text="Send", command=self.send)
		self.send_button.pack(side=tk.RIGHT, pady = 4)
			# bind return to send method
		self.main_window.bind('<Return>',lambda event:self.send())

		# packing
		self.chat_and_username_frame.pack(side=tk.TOP)
		self.send_area_frame.pack(side = tk.LEFT)

		# mainloop and recieve thread
		recieve_thread = threading.Thread(target=self.receive)
		recieve_thread.start()
		self.main_window.mainloop()



	def receive(self):
		while True:
			try:
				message = self.client_socket.recv(1024).decode('ascii')
				if message.startswith("<users>"):
					message = message.removeprefix("<users>")
					self.username_area.delete('1.0', tk.END)
					self.username_area.insert(tk.END, message)
				else:
					self.chat_area.insert(tk.END, message)
					self.chat_area.see(tk.END)
			except:
				print("An error occured!")
				self.client_socket.close()
				break
		


	def send(self):
		message = self.send_area.get()
		self.send_area.delete(0, 'end')
		message = '{}: {}\n'.format(self.username, message)
		self.client_socket.send(message.encode('ascii'))



u1 = Client(HOST,PORT)