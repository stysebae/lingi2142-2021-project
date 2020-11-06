"""
LINGI2142: Computer Networks: Configuration and Management
File: udp_server.py
Authors: Sophie Tysebaert and Dimitri Wauters

This file sets up a simple UDP server.
"""

import socket


class SimpleUDPClient:
    """
    This class represents a simple UDP client.
    """

    def __init__(self, server, buffer_size=1024):
        """
        :param server: (tuple) IPv4 address and port of the server to which to connect.
        :param buffer_size: (int) Size of the buffer (in bytes).
        """
        self.server_ip_address = server[0]
        self.server_port = server[1]
        self.buffer_size = buffer_size
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send(self, message):
        """
        Connect the client to a specific server.
        """
        bytes_to_send = str.encode(message)
        self.socket.sendto(bytes_to_send, (self.server_ip_address, self.server_port))

    def get_server_response(self):
        return self.socket.recvfrom(self.buffer_size)[0]


if __name__ == '__main__':
    client = SimpleUDPClient(("127.0.0.1", 53531))
    # client = SimpleUDPServer(("12.11.0.55", 53))
    client.send("Message sent to a UDP server!")
    print(client.get_server_response())