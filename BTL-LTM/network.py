import socket


class Network:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.client.settimeout(5)  # Set a timeout of 5 seconds
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.timeout:
            raise Exception("Kết nối đã hết thời gian chờ.")
        except Exception as e:
            raise Exception(f"Không thể kết nối tới server: {e}")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
    # Add this method to the Network class in network.py
    def disconnect(self):
        self.client.close()  # Close the connection
        print("Ngăt kết nối từ client")
