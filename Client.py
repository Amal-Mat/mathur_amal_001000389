import time
import socket
import threading
import hashlib
import itertools
import sys
from Crypto import Random
import Crypto.Cipher.AES as AES
from Crypto.PublicKey import RSA

# Setting up socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host and port input user
host = '192.168.253.131'
port = 9000
# binding the address and port
server.connect((host, port))


# public key and private key
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
public = key.publickey().exportKey()
private = key.exportKey()

# hashing the public key
hash_public = hashlib.sha1(public)
hex_digest = hash_public.hexdigest()

server.send(public)
confirm = server.recv(1024)
if confirm == "YES":
    server.send(hex_digest)

# connected msg
msg = server.recv(1024)
print(msg)
en = eval(msg)
decrypt = key.decrypt(en)

# hashing sha1
en_object = hashlib.sha1(decrypt)
en_digest = en_object.hexdigest()

print("\n-----ENCRYPTED PUBLIC KEY AND SESSION KEY FROM SERVER-----")
print(msg)
print("\n-----DECRYPTED SESSION KEY-----")
print(en_digest)
print("\n-----HANDSHAKE COMPLETE-----\n")
while True:
    mess = input("Enter message : ")
    key = en_digest[:16]
    # merging the message and the name
    AESEncrypt = AES.new(key, AES.MODE_CTR, counter=lambda: key)
    eMsg = AESEncrypt.encrypt(mess)
    # converting the encrypted message to HEXADECIMAL to readable
    eMsg = eMsg.encode("hex").upper()
    if eMsg != "" and mess != "exit":
        print("ENCRYPTED MESSAGE TO SERVER-> "+eMsg)
        server.send(eMsg)
    elif mess == "exit":
        server.send(eMsg)
        print("ENCRYPTED MESSAGE TO SERVER-> "+eMsg)
        print("\nSession ended as client sent exit")
        break
    newmess = server.recv(1024)
    print("\nENCRYPTED MESSAGE FROM SERVER-> " + newmess)
    key = en_digest[:16]
    decoded = newmess.decode("hex")
    AESDecrypt = AES.new(key, AES.MODE_CTR, counter=lambda: key)
    dMsg = AESDecrypt.decrypt(decoded)
    if dMsg == 'exit':
        print("\nSession ended as server sent exit")
        break
    else:
        print("\n**New Message From Server**  " +
              time.ctime(time.time()) + " : " + dMsg + "\n")

server.close()
