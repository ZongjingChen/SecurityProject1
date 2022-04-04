from socket import *

MSG_INFECTED = b'\x00'
STEP = 10**7

server_ip = "10.123.144.168"
receive_port = 55554
server_port = 55555

receive_socket = socket(AF_INET, SOCK_DGRAM)
receive_socket.bind(('', receive_port))
send_socket = socket(AF_INET, SOCK_DGRAM)
send_socket.sendto(MSG_INFECTED, (server_ip, server_port))
print('ready')

while True:
    semiprime_msg, _ = receive_socket.recvfrom(2048)
    range_msg, _ = receive_socket.recvfrom(2048)
    

    semiprime = int.from_bytes(semiprime_msg, 'little')
    range_start = int.from_bytes(range_msg, 'little')

    print(f'semiprime: {semiprime}, range: {range_start} - {range_start + STEP - 1}')

    result = -1
    for i in range(range_start, range_start + STEP):
        if i == 0 or i == 1:
            continue
        if i == semiprime:
            break
        if semiprime % i == 0:
            result = int(i)
            send_socket.sendto(result.to_bytes(16, 'little'), (server_ip, server_port))
            print(f'\n<=============SUCCESS. RESULT: {result}=============>\n')
            break
    if result == -1:
        print(f'Failed')
    send_socket.sendto(MSG_INFECTED, (server_ip, server_port))
