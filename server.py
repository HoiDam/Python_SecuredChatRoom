import socket
import random
import sys
from threading import Thread
import json
import base64

# -----
from _aes import AESCipher
from _rsa import RSACipher
# -----

# AES implementation
# password = sys.argv[2] #password
password = "123"

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024)
            host, port = cs.getpeername()
            print(host,":",port,"(Encrypted msg demo): ",msg)
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg)

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

RSAWorker = RSACipher()
RSAWorker.GenerateKey()
SessionKey = str(random.randint(1,10000))   # For message encrypte

if __name__== "__main__":
    client_sockets = set()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)

    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # print("[DEBUG]{}".format(RSAWorker.publicKey))

    while True:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} connected.")
        client_sockets.add(client_socket)

        WelcomePayload = {}
        WelcomePayload["Message"] = "Welcome"
        WelcomePayload["PublicKey"] = RSAWorker.publicKey
        client_socket.send(json.dumps(WelcomePayload).encode("utf8"))

        LoginPayload_Encrypted = client_socket.recv(2048).decode()
        LoginPayload = json.loads(RSAWorker.rsa_decode(LoginPayload_Encrypted))
        # print("[DEBUG]{}".format(RSAWorker.rsa_decode(LoginPayload_Encrypted)))

        Payload = {}
        if password == LoginPayload["PW"]:
            Payload["SessionKey"] = SessionKey
            Payload["Message"] = "Success Login"
            clientAESWorker = AESCipher(str(LoginPayload["OneTimeKey"]))
            print(json.dumps(Payload))
            print(clientAESWorker.encrypt(json.dumps(Payload)))
            client_socket.send(clientAESWorker.encrypt(json.dumps(Payload)))
        else:
            Payload["Message"] = "Fail Login"
            client_socket.send(json.dumps(Payload).encode("utf8"))

        t = Thread(target=listen_for_client, args=(client_socket,))
        t.daemon = True
        t.start()