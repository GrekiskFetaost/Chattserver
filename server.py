import threading #Importing threading to handle multiple clients at once.
import socket #Importing socket for networkcommunication between clients and server.
from colorama import Fore, init
import random

#Initialize colorama to ensure proper color display in the terminal on all OS.
init()
COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.YELLOW, Fore.MAGENTA]

#Server IP-address and portnumber.
host = '127.0.0.1'
port = 55555

#Creating a socket for the server and listening on incoming connections.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#Lists to keep track of connected clients and their nicknames.
clients = [] 
nicknames = []
client_colors = {} #Dictionary for every users color.

def broadcast(msg): #We will broadcast the message to all clients in the list clients.
    for client in clients:
        client.send(msg)


def handle(client): #Handling messages from each client.
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')#Receiving message from the client and decoding it.
            index = clients.index(client) #Find the client index from clientslist.
            nickname = nicknames[index] #Get clients nickname with the indexnumber.

            #Asign a color to the nickname for sending messages if they dont already have a color.
            if nickname not in client_colors:
                color = random.choice(COLORS)
                client_colors[nickname] = color

            color = client_colors[nickname] #Get clients color
            formatted_msg = f"{color}{nickname}: {msg}{Fore.RESET}".encode('utf-8')
            broadcast(formatted_msg) #Sending colored message to all clients.

        except Exception as e: #Error handling for disconnected clients or other errors.
            print(f"Error handling client {client}: {e}")
            try:
                #Remove the client from clientslist and close the connection.
                index = clients.index(client)
                clients.remove(client)
                client.close()
                
                #Get clients nickname and delete it from nicknames list.
                nickname = nicknames[index]
                print(f"{nickname} disconnected.")
                nicknames.remove(nickname)
                del client_colors[nickname] #Remove color from dictionary
                
            except ValueError:
                print("Client already removed.")
            break #Break the loop to stop the handling of a client.

def receive(): #Accepts new connections from clients and starting a new thread for each client.
    while True:
        try:
            client, addr = server.accept() #Waiting for incomming connection and accept when clients connect.
            print(f"Connected with {str(addr)}") #Print information to the server

            client.send('NICK'.encode('utf-8')) #Request the clients nickname
            nickname = client.recv(1024).decode('utf-8')

            #Store nicknames and clients in the lists.
            nicknames.append(nickname)
            clients.append(client)

            broadcast(f"User {nickname} joined the chat!".encode('utf-8'))

            print(f"User {nickname} joined the chat!") #Print to the server when a new user connects
            client.send('Connected to the server!'.encode('utf-8')) #Tell the user that his connection is sucessfull
            
            #Start a new thread to handle the clients messages.
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

        except Exception as e:#Logging any errors when connecting.
            print(f"Error accepting new connection: {e}")

print("Server is listening..")
receive()