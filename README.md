# Instant Messenger

A client-server system that implements an instant messenger using TCP allowing users to chat with each other.

## Running the Program

### Server

To start the server run the following line in the command prompt:

**python server.py [port]**

where [port] is the port that clients will connect through.

### Client

To start the client run the following line in the command prompt:

**python client.py [username] [hostname] [port]**

for example python client.py Lara 127.0.0.1 10000 would allow a client using the username "Lara" to connect to '127.0.0.1' (the local host) via port number 10000.


## Commands

In the client program there are a few basic commands that allow the clients to interact in different ways.

### \<all>

Typing \<all> in a message will broadcast the message to all clients. However, if there is no command in the message, the message will also send to all clients.

### <To [client]>

<To [client]> where [client] is the username of another connected user will send the message to just the one client specified.

### <help>

lists the commands the user can use

### <list>

Lists the users connected to the server

### <access>

Requests access to the server's shared files.
This command must be ran before a client can download files from the server.

### <download [FileName]>

This command will download the file [FileName] from the server.

### \<exit>

This command will cause the client to leave the chat