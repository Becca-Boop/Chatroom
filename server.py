import socket
import threading
import sys
import os

host = '127.0.0.1'
port = sys.argv[1]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, int(port)))
server.listen()

class Client:
    client_username = ''
    client_address = ''
    server_access = False
    def __init__(self, client_sock, client_username, client_address):
        self.client_sock = client_sock
        self.client_username = client_username
        self.client_address = client_address

clients = []

def new_client(client, client_username, client_address):
    print('Attempted connection from unknown client username {}\n'.format(client_username))
    newUser = Client(client, client_username, client_address)
    clients.append(newUser)

def broadcast(message):
    for client in clients:
        client.client_sock.send(message)

def direct(message, c):
    c.send(message)

def file_send(c, file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            message_length = 'len: {}'.format(len(file_data))
            c.sendall(message_length.encode())
            c.sendall(file_data)
            print("File sent successfully")
    except FileNotFoundError:
        print("Error: File not found")
        message = 'File not found'
        c.sendall(message.encode('ascii'))

def handle(client, client_username):
    while True:
        try:
            data = client.recv(1024).decode('ascii')
            sent = False
            if '<exit>' in data:
                client.close()
                sent = True
            elif '<all>' in data:
                message = '\n{}>>{}\n'.format(client_username, data.replace('<all>', '')).encode('ascii')
                broadcast(message)
                sent = True
            elif '<list>' in data: # doesn't work yet
                message = 'Clients Connected:\n'
                for c in clients:
                    message += '{}\n'.format(c.client_username)
                direct(message, client)
                sent = True
            elif '<access>' in data:
                print('{} requested access to Server Shared Files'.format(client_username))
                try:
                    SharedFiles = os.environ["SERVER_SHARED_FILES"]
                except:
                    cwd = os.getcwd()
                    SharedFiles = '{}/SharedFiles'.format(cwd)
                SharedFileDir = os.listdir('{}/SharedFiles'.format(cwd))
                message = 'successful access, number of files in server: {}'.format(str(len(SharedFileDir)))
                for c in clients:
                    if c.client_username == client_username:
                        c.server_access = True
                direct(message.encode('ascii'), client)
                sent = True
            elif '<file' in data:
                access = False
                for c in clients:
                    if c.client_username == client_username:
                        if c.server_access == True:
                            access = True
                if access:
                    file_path = data[6:-1]
                    print('{} requested to download {}'.format(client_username, file_path))
                    message = '<file> {}'.format(file_path).encode('ascii')
                    direct(message, client)
                    file_path = '{}/{}'.format(SharedFiles, file_path)
                    file_send(client, file_path)
                else:
                    message = '{} does not have access to server shared files, request access with <access>'.format(client_username)
                    direct(message.encode('ascii'), client)
                sent = True
            for c in clients:
                if data.find('<To {}>'.format(c.client_username)) != -1:
                    message = '\n{} {}\n'.format(client_username, data.replace('<To {}>'.format(c.client_username), '<DM>>>')).encode('ascii')
                    direct(message, c.client_sock)
                    sent = True
            if sent == False:
                message = '\n{}>> {}\n'.format(client_username, data).encode('ascii')
                broadcast(message)
                sent = True
        except:
            for c in clients:
                if c.client_username == client_username:
                    clients.remove(c)
            client.close()
            broadcast('{} has left the chat!'.format(client_username).encode('ascii'))
            break
    
def receive():
    while True:
        client, client_address = server.accept()
        print("Connected with {}".format(str(client_address)))
        try:
            client.send('NICK'.encode('ascii'))
            client_username = client.recv(1024).decode('ascii')
        except ValueError:
            print("Client did not send a username")
            client.close()
            break

        if len(clients) == 0:
            new_client(client, client_username, client_address)
        else:
            NotAuthorised = True
            j=0
            while NotAuthorised:
                for c in clients:
                    if c.client_username == client_username:
                        user = c
                        NotAuthorised = False
                        break
                if j >= len(clients):
                    new_client(client, client_username, client_address)
                    NotAuthorised = False
                j+=1

        print("Username is {}".format(client_username))
        broadcast("{} has joined the chat!".format(client_username).encode('ascii'))
        data = 'Welcome {}!\n'.format(client_username)
        direct(data.encode('ascii'), client)

        thread = threading.Thread(target=handle, args=(client, client_username))
        thread.start()

print("server is listening")
receive()

# D:\Bex\1 Uni Work\Year 2\Networks and Systems\Coursework 1\chatroom\