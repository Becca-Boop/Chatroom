import socket
import sys
import threading

hostname = sys.argv[2]
port = sys.argv[3]

username = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((hostname, int(port)))
except:
    sys.exit('Error, server at host: {}, port number: {} is unavailable'.format(hostname, port))

def receive_file(message):
    file_name = message[7:]
    file_length = client.recv(1024).decode()
    file_length = int(file_length[5:])
    recv_length = 0
    with open('{}/{}'.format(username, file_name), 'ab') as file:
        while recv_length < file_length:
            file_data = client.recv(1024)
            file.write(file_data)
            recv_length += len(file_data)
        file.close()
        message = 'File received successfully, file size: {}'.format(file_length)
        print('\r ', message)
        print('\r>> ', end='')
        

        

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(username.encode())
            elif '<file>' in message:
                receive_file(message)
            else:
                print('\r ', message)
                print('\r>> ', end='')
        except:
            client.close()
            break

def write():
    while True:
        try:
            print('\r>> ', end='')
            message = input('')
            print('\n')
            client.send(message.encode())
            if '<exit>' in message:
                client.close()
                print("successfully left session")
                sys.exit(0)
        except:
            client.close()
            break
            


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()