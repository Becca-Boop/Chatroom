import socket
import threading
import sys

host = '127.0.0.1'
port = sys.argv[1]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, int(port)))
server.listen()

class Client:
    client_username = ''
    client_address = ''
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
                print(message)
                print(len(clients))
                for c in clients:
                    message += '{}\n'.format(c.client_username)
                print(message)
                direct(message, client)
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