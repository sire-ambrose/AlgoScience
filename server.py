import socket
import yaml
import threading
from _thread import start_new_thread


def read_file() -> str:
    '''
    Reads the 200.txt file and returns the content

    Returns:
        contents (str): the file conent
    '''
    # reading the config file
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
        path = config["linuxpath"]

    # reading and returning the content 200.txt file
    with open(path) as f:
        contents = f.read()

    return contents


def threaded(client : socket.socket):
    """
    Args:
        client(socket.socket): client socket
    """

    while True:

        # server receives "String" from client and decode the content
        # fron byte to string
        msg = client.recv(1024)
        decoded_msg = msg.decode('utf-8')

        # The 200.txt file is read
        file_200txt = read_file()

        # The client input and the file content are compared
        # and the appropaite response is to return
        if decoded_msg in file_200txt:
            response_msg = "STRING EXISTS"

        else:
            response_msg = "STRING NOT FOUND"

        # server sends response to client
        client.sendall(bytes(response_msg, 'utf-8'))

    client.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = 8000

    server.bind((socket.gethostname(), PORT))
    server.listen(5)

    print("socket binded to port", PORT)

    print_lock = threading.Lock()

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        clientsocket, address = server.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', address)

        # Start a new thread
        start_new_thread(threaded, (clientsocket,))
    server.close()


if __name__ == '__main__':
    main()
