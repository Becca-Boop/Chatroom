import socket
import sys
import threading

hostname = sys.argv[2]
port = sys.argv[3]

username = sys.argv[1]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hostname, int(port)))

def receive_file(message):
    file_name = message[7:]
    file_length = client.recv(1024).decode()
    file_length = int(file_length[5:])
    recv_length = 0
    file = open(file_name, 'wb')
    file.close()
    with open(file_name, 'ab') as file:
        while recv_length < file_length:
            file_data = client.recv(1024)
            file.write(file_data)
            recv_length += len(file_data)
        file.close()
        print("File received successfully")
        

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(username.encode('ascii'))
            elif '<file>' in message:
                receive_file(message)
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        #message = input('>> {}: '.format(username))
        message = input('')
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()