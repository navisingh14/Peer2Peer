#/bin/sh

from socket import *
import os
import threading
import thread
import pickle

serverPort = 7765
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print 'the server is ready to receive'


activePeers = {}
RFC = {}


def add_client_to_active_peers(peer_name, upload_port):
    activePeers[peer_name] = upload_port

def add_to_rfc_list(rfc_num, rfc_title, peer_name):
    for i in range(len(rfc_num)):
        if rfc_num[i] in RFC:
            RFC[rfc_num[i]][1].append(peer_name)
        else:
            RFC[rfc_num[i]] = [rfc_title[i],[peer_name]]



def del_client_from_active_peers(peer_name):
    global activePeers
    del(activePeers[peer_name])

def del_from_rfc_list(rfc_num,peer_name):
    global RFC
    for i in range(len(rfc_num)):
        RFC[rfc_num[i]][1].remove(peer_name)



def new_client_thread(connSock, addr):
    global activePeers, RFC
    data = pickle.loads(connSock.recv(4096))
    print data
    upload_port = data[0]
    rfc_num = data[1]
    rfc_title = data[2]
    add_client_to_active_peers(addr[0], upload_port)
    add_to_rfc_list(rfc_num, rfc_title, addr[0])
    print '\n'
    print activePeers
    print RFC
    print '\n'
    while True:
        print len(connSock.recv(1024))
        if(len(connSock.recv(1024)) == 0):
            del_client_from_active_peers(addr[0])
            del_from_rfc_list(rfc_num, addr[0])
            print activePeers
            print RFC
            print 'closed'
            break
    connectionSocket.close()
    



#Master Socket listening forever
while 1:
    connectionSocket, addr = serverSocket.accept()
    thread.start_new_thread(new_client_thread, (connectionSocket,addr))
