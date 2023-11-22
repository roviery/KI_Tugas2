import socket
import threading

class ChatServer:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client_sockets = []
    self.lock = threading.Lock()
    self.start_server()

  def start_server(self):
    self.server_socket.bind((self.host, self.port))
    self.server_socket.listen(2)
    print(f"Server listening on {self.host}:{self.port}")

    while True:
      client_socket, client_address = self.server_socket.accept()
      print(f"Accepted connection from {client_address}")

      with self.lock:
          self.client_sockets.append(client_socket)

      client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
      client_thread.start()

  def broadcast_message(self, message, sender_socket):
    with self.lock:
      for client_socket in self.client_sockets:
        if client_socket != sender_socket:
          try:
            client_socket.send(message.encode())
          except socket.error:
            self.client_sockets.remove(client_socket)

  def handle_client(self, client_socket):
    while True:
      try:
        message = client_socket.recv(1024).decode()
        if not message:
          break
        print(f"Received message: {message}")
        self.broadcast_message(message, client_socket)
      except socket.error:
        # Handle disconnection
        with self.lock:
          self.client_sockets.remove(client_socket)
        break

    print("Client disconnected")
    client_socket.close()

if __name__ == "__main__":
  server = ChatServer("127.0.0.1", 5555)