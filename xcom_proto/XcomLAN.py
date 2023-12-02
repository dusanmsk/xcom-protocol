#! /usr/bin/env python3

import socket
import logging

from concurrent.futures import ThreadPoolExecutor

from .protocol import Package
from .XcomAbs import XcomAbs

##
# Class abstracting Xcom-LAN TCP network protocol
##

class XcomLANTCP(XcomAbs):

    def __init__(self, port=4001):
        """
        MOXA is connecting to the TCP Server we are creating here.

        Once it is connected we can send package requests.
        """

        self.localPort = port
        self.log = logging.getLogger("XcomLANTCP")

    def __enter__(self):
        self.log.info(f"Starting TCP server on port {self.localPort}")

        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServer.bind(("", self.localPort))
        self.tcpServer.listen(1)

        self.log.info("Waiting for MOXA to connect...")
        
        conn, addr = self.tcpServer.accept()
        self.log.debug(f"Got connection from {addr}")

        self.conn = conn

        # TODO handshake with GUID (?)
        return self

    def __exit__(self, *_):
        self.conn.close()
        self.tcpServer.close()
        return True

    def sendPackage(self, package: Package) -> Package:
        data: bytes = package.getBytes()
        
        self.log.debug(f" --> {data.hex()}")
        self.conn.send(data)

        response: bytes = self.conn.recv(256)
        self.log.debug(f" <-- {response.hex()}")
        
        retPackage = Package.parseBytes(response)
        self.log.debug(retPackage)

        # MOXA sometimes sends unrelated data, so we need to ignore those
        # and resent our request
        try:
            assert retPackage.isResponse()
            assert retPackage.frame_data.service_id == package.frame_data.service_id
            assert retPackage.frame_data.service_data.object_id == package.frame_data.service_data.object_id
        except AssertionError:
            return self.sendPackage(package)

        if err := retPackage.getError():
            raise KeyError("Error received", err)

        return retPackage


class XcomLANTCP_crap(XcomAbs):

    def __init__(self, serverIP: str, dstPort=4002, srcPort=4001, localPort=5000):
        """
        Package requests are being sent to serverIP : dstPort using TCP protocol.

        The srcPort is needed for the server to listen to the TCP responses locally.
        """

        self.serverAddress = (serverIP, dstPort)
        self.clientPort = srcPort
        self.localPort = localPort
        self.log = logging.getLogger("XcomLAN")

        self.tcpListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpListener.bind(("", self.localPort))
        self.tcpListener.listen(1)

    def sendPackage(self, package: Package) -> Package:
        data: bytes = package.getBytes()

        with ThreadPoolExecutor() as listener, \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender:
            self.log.debug(f" --> {data.hex()}")

            future = listener.submit(self._awaitTCPResponse, self.tcpListener)

            sender.connect(self.serverAddress)
            sender.sendall(data)

            connection, address = future.result(10)
            value = connection.recv(256)
            connection.close()

            self.log.debug(f" <-- {value}")

        if not value:
            raise ValueError("Package listener returned None")

        retPackage = Package.parseBytes(value)
        self.log.debug(retPackage)

        if err := retPackage.getError():
            raise KeyError("Error received", err)

        return retPackage

    def _awaitTCPResponse(self, tcpListener: socket.socket) -> tuple:
        try:
            connection, address = tcpListener.accept()
        except socket.timeout:
            self.log.error("Waiting for response from XcomLAN timed out")
            raise

        return connection, address


##
# Class abstracting Xcom-LAN UDP network protocol
##

class XcomLANUDP(XcomAbs):

    def __init__(self, serverIP: str, dstPort=4002, srcPort=4001):
        """
        Package requests are being sent to serverIP : dstPort using UDP protocol.

        The srcPort is needed, because XcomLAN will send the UDP response NOT
        to the corresponding UDP source endpoint (like every fucking server on this
        planet would do) but rather to <yourIP> : srcPort.

        So in order to make this work, we need to listen on srcPort for incoming
        data.
        """

        self.serverAddress = (serverIP, dstPort)
        self.clientPort = srcPort
        self.log = logging.getLogger("XcomLAN")

        self.udpListener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpListener.bind(("", self.clientPort))
        self.udpListener.settimeout(2) # as recommended by Studer Xcom documentation

    def sendPackage(self, package: Package) -> Package:
        data: bytes = package.getBytes()
        
        with ThreadPoolExecutor() as listener, \
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
            self.log.debug(f" --> {data.hex()}")

            future = listener.submit(self._awaitUDPResponse, self.udpListener)

            sender.sendto(data, self.serverAddress)

            value = future.result(10) 
            self.log.debug(f" <-- {value}")

        if not value:
            raise ValueError("Package listener returned None")

        retPackage = Package.parseBytes(value)
        self.log.debug(retPackage)

        if err := retPackage.getError():
            raise KeyError("Error received", err)
        
        return retPackage

    def _awaitUDPResponse(self, udpSocket: socket.socket) -> bytes:
        try:
            response = udpSocket.recv(256)
        except socket.timeout:
            self.log.error("Waiting for response from XcomLAN timed out")
            raise

        return response
