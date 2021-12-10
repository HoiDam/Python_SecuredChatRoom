import socket
import random
import time
from threading import Thread
from datetime import datetime
from Crypto import PublicKey
from colorama import Fore, init, Back
import json
import base64

# -----
from _aes import AESCipher
from _rsa import RSACipher
# -----

def listen_for_messages():
    while True:
        message = s.recv(1024)
        message = AESWorker.decrypt(message)
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
RSAWorker = RSACipher()

if __name__== "__main__":
    

    # initialize TCP socket
    s = socket.socket()
    print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))

    # Getting welcome payload
    WelcomePayload = json.loads(s.recv(1024).decode("utf8"))
    # print(WelcomePayload)

    password = input("[?] Password: ")
    LoginPayload = {}
    LoginPayload["PW"] = str(password)
    LoginPayload["OneTimeKey"] = str(random.randint(1,10000))
    # print(json.dumps(LoginPayload))
    
    ServerPublicKey = WelcomePayload['PublicKey']
    RSAWorker.PublicKeyImport(ServerPublicKey)
    s.send(RSAWorker.rsa_encode(json.dumps(LoginPayload)).encode("utf-8"))
    # print(LoginPayload)

    LoginAESWorker = AESCipher(str(LoginPayload["OneTimeKey"]))
    Payload = json.loads(LoginAESWorker.decrypt(s.recv(1024).decode("utf8")))
    if Payload["Message"] == "Fail Login":
        print("[-] Wrong PW")
        s.close()
        exit()
    else:
        print("[+] Connected")
        AESWorker = AESCipher(str(Payload["SessionKey"]))

    name = input("[?] Enter your name: ")
    t = Thread(target=listen_for_messages)
    t.daemon = True
    t.start()

    while True:
        Message = input()
        if Message.lower() == 'q':
            break

        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"{client_color}[{date_now}] {name}{separator_token}{Message}{Fore.RESET}"
        
        to_send = AESWorker.encrypt(to_send)
        s.send(to_send)

    # s.close()
