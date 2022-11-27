import socket
import sys
import traceback
from threading import Thread
import yaml


def main():
    start_server()


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

def start_server():
    host = "127.0.0.1"
    port = 8000  # arbitrary  port
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")

    # Bind To Port
    try:
        soc.bind((host, port))
    except Exception as e:
        print("Bind failed. Error : " + e)
        sys.exit()

    soc.listen(6)  # queue up to 6 requests
    print("Socket now listening")
    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except Exception as e:
            print("Thread did not start. Error: " + e)
            traceback.print_exc()
        soc.close()


def client_thread(connection, ip, port, max_buffer_size=1240):
    is_active = True
    while is_active:
        client_input = process_input(connection, max_buffer_size)
        if "--QUIT--" in client_input:
            print("Client is requesting to quit")
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        else:
            connection.sendall(client_input.encode("utf8"))


def process_input(connection: socket.socket, max_buffer_size: int) -> str:
    """This function takes in the input text from client, 
    checks for the string in the 200k.txt file and sends STRING EXIST/STRING DOES NOT EXIST 
    depending on the processing

    Args:
        connection (socket.socket): The client connection
        max_buffer_size (int): The input size

    Returns:
        str: STRING EXIST or STRING DOES NOT EXIST response
    """    
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print(f"The input size is greater than expected {client_input_size}")
    decoded_input = client_input.decode("utf8").rstrip()
    # The 200.txt file is read
    file_200txt = read_file()

    # The client input and the file content are compared
    # and the appropaite response is to return
    if decoded_input in file_200txt:
        response_msg = "STRING EXISTS"

    else:
        response_msg = "STRING NOT FOUND"

    return response_msg




if __name__ == "__main__":
    main()
