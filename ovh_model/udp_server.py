#!/usr/bin/env python3

"""
LINGI2142: Computer Networks: Configuration and Management
File: udp_server.py
Authors: Sophie Tysebaert and Dimitri Wauters

This file sets up a simple UDP server.
"""

import socket


class SimpleUDPServer:
    """
    This class represents a simple UDP server (e.g. DNS server).
    """

    def __init__(self, ip_address, port, buffer_size=1024):
        """
        :param ip_address: (str) An IPv4 address.
        :param port: (int) A port.
        :param buffer_size: (int) Size of the buffer (in bytes).
        """
        self.ip_address = ip_address
        self.port = port
        self.buffer_size = buffer_size

    def run(self):
        """
        Run a UDP server.
        """
        # Create a socket and bind it to the given IP address and port
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        server_socket.bind((self.ip_address, self.port))
        print("UDP server up and listening")
        bytes_to_send = str.encode("Hey UDP client!")
        while True:
            bytes_received = server_socket.recvfrom(self.buffer_size)
            message = bytes_received[0]
            client_address = bytes_received[1]
            client_message = f"Message from client: {message}"
            client_ip_address = f"Client IP address: {client_address}"
            print(client_message)
            print(client_ip_address)
            server_socket.sendto(bytes_to_send, client_address)


if __name__ == '__main__':
    #server = SimpleUDPServer("192.168.1.46", 53)
    server = SimpleUDPServer("12.11.0.55", 53)
    server.run()
