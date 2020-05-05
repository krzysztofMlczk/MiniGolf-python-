import socket
import pickle


class Network:
    def __init__(self, config):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = config["server"]
        self.port = config["port"]
        self.address = (self.server, self.port)
        self.player = self.connect()

    def get_id(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048))

        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))

        except socket.error as e:
            print(e)

    def listen(self):
        try:
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)