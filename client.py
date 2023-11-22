import socket
import threading
from DES import encrypt, decrypt

class ChatClient:
  def __init__(self, host, port, username):
    self.host = host
    self.port = port
    self.username = username
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect_to_server()

  def connect_to_server(self):
    self.client_socket.connect((self.host, self.port))
    print(f"Connected to server on {self.host}:{self.port}")

    # Start a separate thread for receiving messages
    receive_thread = threading.Thread(target=self.receive_messages)
    receive_thread.start()

    # Start the main thread for sending messages
    self.send_messages()

  def receive_messages(self):
    while True:
      try:
        encrypted_message = self.client_socket.recv(1024).decode()
        if not encrypted_message:
          break
        print(f"encrypted message is {encrypted_message}")
        decrypted_message = decrypt(encrypted_message)
        print(f"decrypted message is {decrypted_message}")
      except socket.error:
        print("Connection lost")
        break

  def send_messages(self):
    while True:
      message = input("")
      encrypted_message = encrypt(message)
      self.client_socket.send(encrypted_message.encode())

if __name__ == "__main__":
  username = input("Enter your username: ")
  client = ChatClient("127.0.0.1", 5555, username)
