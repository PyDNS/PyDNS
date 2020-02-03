import socket
from pydns.utils.log import logger


class Server:

    def __init__(self, port=53, ip='127.0.0.1'):
        self.port = port
        self.ip = ip

        # Initialize udp ipv4 socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))

        logger.info("Server started on port " + str(self.port))

        while 1:
            self.data, self.addr = self.sock.recvfrom(512)
            print(self.data)
