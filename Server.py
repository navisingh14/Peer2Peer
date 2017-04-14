#/bin/sh

from socket import *
import os
import threading
import thread
import pickle

serverPort = 7754
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print 'the server is ready to receive'


activePeers = {}
RFC = {}


def add_client_to_active_peers(peer_name, upload_port):
    activePeers[peer_name] = upload_port

def add_to_rfc_list(rfc_num, rfc_title, peer_name):
    if rfc_num in RFC:
        RFC[rfc_num][1].append(peer_name)
    else:
        RFC[rfc_num] = [rfc_title,[peer_name]]


def new_client_thread(connSock, addr):
    global activePeers, RFC
    data = pickle.loads(connectionSocket.recv(1024))
    upload_port = data[0]
    rfc_num = data[1]
    rfc_title = data[2]
    add_client_to_active_peers(addr[0], upload_port)
    add_to_rfc_list(rfc_num, rfc_title, addr[0])
    print '\n'
    print activePeers
    print RFC
    print '\n'
    connectionSocket.close()
    



#Master Socket listening forever
while 1:
    print activePeers
    print RFC
    connectionSocket, addr = serverSocket.accept()
    thread.start_new_thread(new_client_thread, (connectionSocket,addr))
