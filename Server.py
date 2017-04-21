#/bin/sh

import socket
import os
import threading
import thread
import pickle

serverPort = 5678
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print 'the server is ready to receive'

#peer_name and upload_port
activePeers = {}

#rfc_num, rfc_title, peer_name
RFC = {}


def add_client_to_active_peers(peer_name, upload_port):
    global activePeers
    activePeers[peer_name] = upload_port

def add_to_rfc_list(rfc_num, rfc_title, peer_name):
    global RFC
    if rfc_num in RFC:
        RFC[rfc_num][1].append(peer_name)
    else:
        RFC[rfc_num] = [rfc_title,[peer_name]]



def del_client_from_active_peers(peer_name):
    global activePeers
    del(activePeers[peer_name])

def del_from_rfc_list(peer_name):
    global RFC
    for rfc_num in RFC:
        if peer_name in RFC[rfc_num][1]:
            RFC[rfc_num][1].remove(peer_name)


def add_invalid(data):
    answer = False
    compare = {0:'ADD',
               1:'RFC',
               3:'P2P-CI/1.0',
               4:'Host:',
               6:'Port:',
               8:'Title:'
               }
    for key, value in compare.iteritems():
        if(data[key] != value):
            answer = True
            break
    return answer
    
    pass

def lookup_invalid(data):
    answer = False
    compare = {0:'LOOKUP',
               1:'RFC',
               3:'P2P-CI/1.0',
               4:'Host:',
               6:'Port:',
               8:'Title:'
               }
    for key, value in compare.iteritems():
        if(data[key] != value):
            answer = True
            break
    return answer

def list_invalid(data):
    answer = False
    compare = {0:'LIST',
               1:'ALL',
               2:'P2P-CI/1.0',
               3:'Host:',
               5:'Port:'
               }
    for key, value in compare.iteritems():
        if(data[key] != value):
            answer = True
            break
    return answer




def checkValidity(data):
    global RFC
    analyse = data.replace("\n"," ").split(" ")
    #check for 505
    if(data.find('P2P-CI/1.0') == -1):
        status = '505'
        phrase = 'P2P-CI Version Not Supported'
    elif((add_invalid(analyse)) and (list_invalid(analyse)) and (lookup_invalid(analyse))): #check for 400
        status = '400'
        phrase = 'Bad Request'
    elif(analyse[0] == 'LOOKUP' and (analyse[2] not in RFC)):
        status = '404'
        phrase = 'Not Found'
    else:
        status = '200'
        phrase = 'OK'
    response_header = "P2P-CI/1.0 " + status + " " + phrase + "\n"
    return response_header, status



def list_response(connSock, response_header):
    global RFC
    global activePeers
    response_body = response_header
    for rfc_num, value in RFC.iteritems():
        for each_peer in value[1]:
            response_body = response_body + "RFC " + str(rfc_num) + " " + str(value[0]) + " " + str(each_peer)+ " " + str(activePeers[each_peer]) + "\n"
    connSock.send(response_body)
    pass
    
def add_response(connSock, data, response_header, upload_port, peer_name):
    rfc_num = data[data.find("RFC")+4:data.find("P2P-CI")-1]
    rfc_title = data[data.find("Title:")+6:len(data)-1]
    add_to_rfc_list(rfc_num, rfc_title, peer_name)
    response_body = response_header+ "RFC " + str(rfc_num) + " " + str(rfc_title) + " " + str(peer_name) + " " + str(upload_port) + "\n"
    connSock.send(response_body)
    
#peer_name and upload_port
activePeers = {}

#rfc_num, rfc_title, peer_name
RFC = {}

def lookup_response(connSock, response_header, rfc_num):
    global RFC
    global activePeers
    response_body = response_header
    for each_peer in RFC[rfc_num][1]:
        response_body = response_body + "RFC " + str(rfc_num) + " " + str(RFC[rfc_num][0]) + " " + str(each_peer)+ " " + str(activePeers[each_peer]) + "\n"
    connSock.send(response_body)


def new_client_thread(connSock, addr):
    global activePeers, RFC
    data = pickle.loads(connSock.recv(4096))
    peer_name = addr[0]
    upload_port = data[0]
    #rfc_list = data[0]
    add_client_to_active_peers(peer_name, upload_port)
    #print type(data)
    #print addr[0]
    #print type(addr)
    #print data[1]
    #print data[0]
    connSock.send("Welcome, " + str(addr))
    #print activePeers
    #print RFC
    try:
        while True:
            data = pickle.loads(connSock.recv(4096))
            print (data)
            response_header, status = checkValidity(data)
            request = data.split(" ")[0]
            rfc_num = data[data.find("RFC")+4:data.find("P2P-CI")-1]
            if status=='505' or status == '400' or status == '404':
                connSock.send(response_header)
            elif status == '200':
                if request == 'ADD':
                    add_response(connSock,data, response_header, upload_port, peer_name)
                elif request == 'LOOKUP':
                    print 'LOOKUP'
                    lookup_response(connSock, response_header, rfc_num)
                elif request == 'LIST':
                    list_response(connSock, response_header)
            print len(data)
            if(len(data) == 0):
                del_client_from_active_peers(addr[0])
                del_from_rfc_list(addr[0])
                print activePeers
                print RFC
                print 'closed'
                break
        connectionSocket.close()
    except EOFError:
        print 'closed'
        del_client_from_active_peers(addr[0])
        del_from_rfc_list(addr[0])
        print activePeers
        print RFC
        connectionSocket.close()
    except socket.error as error:
        print 'ungraceful exit'
        print error
        del_client_from_active_peers(addr[0])
        del_from_rfc_list(addr[0])
        print activePeers
        print RFC
        connectionSocket.close()
        

''' upload_port = data[0]
    rfc_num = data[1]
    rfc_title = data[2]
    add_client_to_active_peers(addr[0], upload_port)
    add_to_rfc_list(rfc_num, rfc_title, addr[0])
    print '\n'
    print activePeers
    print RFC
    print '\n'
    '''
    



#Master Socket listening forever
while 1:
    connectionSocket, addr = serverSocket.accept()
    thread.start_new_thread(new_client_thread, (connectionSocket,addr))
