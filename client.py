import socket
import random
import time
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# -----
from _aes import AESCipher
# -----

def listen_for_messages():
    while True:
        message = s.recv(1024)
        message = cipher.decrypt(message)
        message = message.replace(separator_token, ": ")
        print("\n" + message)

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

password = input("[?] Password: ")

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

s.send(password.encode("utf8"))
key = s.recv(1024).decode("utf8")
# print("key:",key)

if key == "Failed":
    print("[-] Wrong Credentials")
else:
    print("[+] Connected.")
    cipher = AESCipher(str(key))


    # prompt the client for a name
    name = input("[?] Enter your name: ")

    # make a thread that listens for messages to this client & print them
    t = Thread(target=listen_for_messages)
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

    while True:
        # input message we want to send to the server
        to_send =  input()
        # a way to exit the program
        if to_send.lower() == 'q':
            break
        
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
        
        to_send = cipher.encrypt(to_send)
        
        # finally, send the message
        s.send(to_send)

    # close the socket
    s.close()
