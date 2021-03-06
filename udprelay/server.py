# A snoob udp relay server
# This file aim to bypass NAT
# run this on server which have public IP
# 2017-12-12

import socket
from .header import decode, encode
from .logger import getLogger
import traceback
logger = getLogger('[server]')


class Server:
    def __init__(self, port=10002):
        self.__running = True
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind(('0.0.0.0', port))
        self.__client_address = ()
        logger.info('server start on ' + str(port))

    def start(self):
        while self.__running:
            data, address = self.__sock.recvfrom(4096)
            if data:
                decode_data, decode_address = decode(data)
                if decode_address != 0:    # From our client
                    self.forword(decode_data, decode_address, address)
                else:
                    if len(self.__client_address) == 0:
                        logger.error('无client!')
                    else:
                        logger.info('Forword back:\t' + str(address) + '\t->\t' +
                                    str(self.__client_address) + ' || ' + str(data))
                        self.__sock.sendto(encode(data, address), self.__client_address)
        self.__sock.close()
    def forword(self, decode_data, decode_address, address):
        self.__client_address = address
        logger.info('Forword\t' + str(address) + '\t->\t' +
                    str(decode_address) + ' data:' + str(decode_data))
        # ('74.205.156.64', 0)
        try:
            self.__sock.sendto(decode_data, decode_address)
        except Exception as e:
            logger.error(traceback.format_exc() + "sendError: des addr: " + str(decode_address))
    def close(self):
        self.__running = False

if __name__ == '__main__':
    server = Server()
    server.start()
