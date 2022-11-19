import socket

client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT= 8000
client.connect((socket.gethostname(), PORT))

while True:
    check_string= input('>>> Enter STRING: ')
    # client sends "String" to server
    client.send(bytes(check_string, 'utf-8'))

    # server receives data from server
    msg= client.recv(1024)
    print(msg.decode('utf-8'))