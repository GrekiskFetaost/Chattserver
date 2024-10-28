import socket #To make network communication possible with the server.
import threading #Importing threading to handle both incoming and outgoing messages at the same time.
from colorama import init

#Initialize colorama to ensure proper color display in the terminal on all OS.
init()
nickname = input("Choose a nickname: ") #Ask the client for a nickname.

#Create a socket for the client and connect to the server IP and PORT.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive(): #The function is handling incoming messages from the server.
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'NICK':
                client.send(nickname.encode('utf-8')) #Send the nickname
            else:
                print(msg) #Show incomming message.

        except Exception as e: #If error occurs the exception will catch it.
            print(f"An error occurred while receiving data: {e}")
            client.close()
            break

def write(): #The function making it possible for clients to send messages to the server.
    while True:
        try:
            msg = f'{nickname}: {input("")}' #Format the messages with clients nickname and send it to the server.
            client.send(msg.encode('utf-8')) #Send message to server
            print("\033[F\033[K", end="") #Clear the message writen from the client
        except Exception as e: #Handle errors when trying to send a message.
            print(f"An error occured while sending data {e}")
            client.close()
            break

#Starting two threads, one to handle receiving messages and one for sending messages.
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()