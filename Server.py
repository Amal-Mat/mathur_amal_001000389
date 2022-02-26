import socket
import hashlib
import os
import time
import sys
import Crypto.Cipher.AES as AES
from Crypto.PublicKey import RSA

host = '192.168.253.131'
port = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)
client, address = server.accept()
print("CLIENT IS CONNECTED. CLIENT'S ADDRESS ->", address)
print("\n-----WAITING FOR PUBLIC KEY & PUBLIC KEY HASH-----\n")
# client's message(Public Key)
getpublickey = client.recv(2048)

# conversion of string to KEY
server_public_key = RSA.importKey(getpublickey)

# hashing the public key in server side for validating the hash from client
hash_pubkey = hashlib.sha1(getpublickey)
hex_digest = hash_pubkey.hexdigest()

if getpublickey != "":
    print(getpublickey)
    client.send("YES")
    gethash = client.recv(1024)
    print("\n-----HASH OF PUBLIC KEY----- \n"+gethash)
if hex_digest == gethash:
    # creating session key
    key_128 = os.urandom(16)
    # encrypt CTR MODE session key
    en = AES.new(key_128, AES.MODE_CTR, counter=lambda: key_128)
    encrypto = en.encrypt(key_128)
    # hashing sha1
    en_object = hashlib.sha1(encrypto)
    en_digest = en_object.hexdigest()

    print("\n-----SESSION KEY-----\n"+en_digest)

    # encrypting session key and public key
    E = server_public_key.encrypt(encrypto, 16)
    print("\n-----ENCRYPTED PUBLIC KEY AND SESSION KEY-----\n"+str(E))
    print("\n-----HANDSHAKE COMPLETE-----")
    client.send(str(E))

    while True:

        # message from client
        newmessage = client.recv(1024)
        # decoding the message from HEXADECIMAL to decrypt the encrypted version of the message only
        decoded = newmessage.decode("hex")
        # making en_digest(session_key) as the key
        key = en_digest[:16]
        print("\nENCRYPTED MESSAGE FROM CLIENT -> "+newmessage)
        # decrypting message from the client
        enc = AES.new(key, AES.MODE_CTR, counter=lambda: key)
        dMsg = enc.decrypt(decoded)
        if dMsg == "exit":
            print("\nMESSAGE FROM CLIENT -> "+dMsg)
            print("\nSession ended as client sent exit")
            break
        else:
            print("\n**New Message**  "+time.ctime(time.time()) + " > "+dMsg+"\n")

        message = input("\nMessage To Client -> ")
        key = en_digest[:16]
        enc = AES.new(key, AES.MODE_CTR, counter=lambda: key)
        eMsg = enc.encrypt(message)
        eMsg = eMsg.encode("hex").upper()
        if eMsg != "" and message != "exit":
            print("ENCRYPTED MESSAGE TO CLIENT-> " + eMsg)
            client.send(eMsg)
        elif message == "exit":
            client.send(eMsg)
            print("\nSession ended as server sent exit")
            break
    client.close()
    server.close()
else:
    print("\n-----PUBLIC KEY HASH DOESN'T MATCH-----\n")
