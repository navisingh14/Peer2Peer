#!/usr/bin/python

import socket
import random
import thread
import pickle
import sys
import getopt
import os
import glob
import platform
import time

#Setting up UploadServer


def setupUploadServer(port):
    uploadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    uploadSocket.bind(('',port))
    #print 'listening'
    uploadSocket.listen(5)
    while True:
        connectionSocket, addr = uploadSocket.accept()
        request = connectionSocket.recv(4096)
        respondToRequest(connectionSocket,request)

def checkValidity(data):
    global RFC
    analyse = data.replace("\n"," ").split(" ")
    rfc_num = analyse[2]
    OS = platform.system()
    current_path = os.getcwd()
    if OS == "Windows":
        filename = current_path + "\\rfc\\RFC_" + rfc_num + "*"
    else:
        filename = current_path + "/rfc/RFC_" + rfc_num + "*"
    if(data.find('P2P-CI/1.0') == -1):
        status = '505'
        phrase = 'P2P-CI Version Not Supported'
    elif(get_invalid(analyse)): #check for 400
        status = '400'
        phrase = 'Bad Request'
    elif(glob.glob(filename)==[]):
        status = '404'
        phrase = 'Not Found'
    else:
        status = '200'
        phrase = 'OK'
    response_header = "P2P-CI/1.0 " + status + " " + phrase + "\n"
    return response_header, status

def get_invalid(data):
    answer = False
    compare = {0:'GET',
               1:'RFC',
               3:'P2P-CI/1.0',
               4:'Host:',
               6:'OS:'
               }
    for key, value in compare.iteritems():
        if(data[key] != value):
            answer = True
            break
    return answer



def respondToRequest(connectionSocket, data):
    #print data
    response_header, status = checkValidity(data)
    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    OS = platform.system()
    analyse = data.replace("\n"," ").split(" ")
    rfc_num = analyse[2]
    if status == '505' or status == '400' or status == '404':
        response = response_header + "Date:" + current_time + "\n" + "OS: "+str(OS)+"\n"
        connectionSocket.send(response)
    else:
        OS = platform.system()
        current_path = os.getcwd()
        if OS == "Windows":
            filename = current_path + "\\rfc\\RFC_" + str(rfc_num) + "*"
        else:
            filename = current_path + "/rfc/RFC_" + str(rfc_num) + "*"
        File = glob.glob(filename)
        last_modified = time.ctime(os.path.getmtime(File[0]))
        content_length = os.path.getsize(File[0])
        response = response_header + "Date:" + current_time + "\n" + "OS: "+str(OS)+"\n"\
                  "Last-Modified: " + last_modified + "\n"\
                  "Content-Length: " + str(content_length) + "\n"\
                  "Content-Type: text/text \n"
        connectionSocket.send(response)        
        txt = open(File[0], 'rb')
        line = txt.read(1024)
        while(line):
            connectionSocket.send(line)
            line = txt.read(1024)        
    connectionSocket.close()
    
    

def getUploadSocket():
    port = random.randint(7000,8000)
    return port


def get(rfc_num, rfc_title, download_host,download_port):
    success = False
    OS = platform.system()
    request_body = "GET RFC "+str(rfc_num)+" P2P-CI/1.0\n"\
              "Host: "+str(download_host)+"\n"\
              "OS: "+str(os)+"\n"
    downloadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    downloadSocket.connect((download_host, int(download_port)))
    downloadSocket.send(request_body)
    #get response back from client
    received_data= downloadSocket.recv(4096)
    print received_data
    if OS == 'Windows':
        if not (os.path.isdir(os.getcwd()+"\\rfc")):
            os.makedirs(os.getcwd()+"\\rfc")
        filename = os.getcwd() + "\\rfc\\RFC_"+str(rfc_num)+"_"+rfc_title+".txt"
    else:
        if not (os.path.isdir(os.getcwd()+"/rfc")):
            os.makedirs(os.getcwd()+"/rfc")
        filename = os.getcwd() + "/rfc/RFC_"+str(rfc_num)+"_"+rfc_title+".txt"
    if(received_data.find("200 OK") != -1):
        received_data = downloadSocket.recv(4096)
        f = open(filename, 'wb')
        while(received_data):
            f.write(received_data)
            received_data = downloadSocket.recv(4096)
        f.close()
        print 'File received successfully'
        success = True
    downloadSocket.close()
    return success
    
''' s.send(bytes(data, 'utf-8'))
    data_rec= pickle.loads(s.recv(1024))
    print("Data_rec", str(data_rec))
    #my_data = data_rec.decode('utf-8')
    my_data = data_rec[1]
    print(my_data)
    current_path = os.getcwd()
    filename = "rfc"+rfc_num+".txt"
    OS = platform.system()
    if OS == "Windows":  # determine rfc path for two different system
        filename = current_path + "\\rfc\\" + filename
    else:
        filename = current_path + "/rfc/" + filename
    #f = open(filename,'w')
    with open(filename, 'w') as file:
        file.write(my_data)
    #f.write(data_rec.decode('utf-8'))
    #f.close()
    s.close()'''





def lookup(clientSocket, rfc_num, rfc_title):
    request_body = "LOOKUP RFC " + str(rfc_num)+" P2P-CI/1.0\n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(rfc_title)+"\n"
    clientSocket.send(pickle.dumps(request_body))
    available_peers = (clientSocket.recv(4096))
    print available_peers

def add(clientSocket, rfc_num, rfc_title):
    request_body = "ADD RFC " + str(rfc_num)+" P2P-CI/1.0\n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(rfc_title)+"\n"
    data = pickle.dumps(request_body)
    clientSocket.send(data)

def list_rfc(clientSocket):
    request_body = "LIST ALL P2P-CI/1.0\n"\
              "Host: "+str(host)+"\n"\
              "Port: "+str(port)+"\n"
    data = pickle.dumps(request_body)
    clientSocket.send(data)
    response = clientSocket.recv(4096)
    print response
 

def local_rfcs():
    local_rfc = {}
    cwd = os.getcwd()
    if platform.system() == 'Windows':
        for each_rfc in glob.glob(cwd + "\\rfc\\RFC*.txt"):
            rfc = each_rfc.split("_")
            local_rfc[rfc[1]]=rfc[2]
    else:
        for each_rfc in glob.glob(cwd + "/rfc/RFC*.txt"):
            rfc = each_rfc.split("_")
            local_rfc[rfc[1]]=rfc[2]
    return local_rfc
    

def addLocalRFC(port, clientSocket):
    available_rfcs = local_rfcs()
    for num, title in available_rfcs.iteritems():
        add(clientSocket, num, available_rfcs[str(num)])
        response = clientSocket.recv(4096)
        print response
    

#Contacting Server
def ContactServer(port, clientSocket):
    try:
        user_input = raw_input("> Enter the command: ADD, LIST, LOOKUP, EXIT:\n")
        if user_input == 'ADD':
            local_rfc = local_rfcs()
            print "List of available RFCs on local system"
            for num, title in local_rfc.iteritems():
                print num, title
            rfc_num = input("Enter the RFC number: ")
            add(clientSocket, rfc_num, local_rfc[str(rfc_num)])
            response = (clientSocket.recv(4096))
            print response
            ContactServer(port, clientSocket)
        elif user_input == 'LIST':
            list_rfc(clientSocket)
            ContactServer(port, clientSocket)
        elif user_input == 'LOOKUP':
            rfc_num = input("Enter the RFC number: ")
            rfc_title = raw_input("Enter the RFC title: ")
            lookup(clientSocket, rfc_num, rfc_title)
            usr_inp = raw_input("Select an option- GET, EXIT, BACK: \n")
            if usr_inp == 'GET':
                download_host = raw_input("Enter the host name: ")
                download_port = input("Enter the port number: ")
                success = get(rfc_num, rfc_title, download_host, download_port)
                if(success):
                    add(clientSocket, rfc_num, rfc_title)
                    response = clientSocket.recv(4096)
                    print response
                ContactServer(port, clientSocket)
            elif usr_inp == 'BACK':
                ContactServer(port, clientSocket)
            elif user_input == 'EXIT':
                clientSocket.close()
        elif user_input == 'EXIT':
            clientSocket.close()
    except Exception, e:
        print type(e)
        print e


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'usage: ./client <server-ip> <server-port>'
        sys.exit()
    opts,args = getopt.getopt(sys.argv[1:], "d:p")
    print type(int(args[1]))
    port = getUploadSocket()
    print port
    thread.start_new_thread(setupUploadServer, (port,))
    serverName = args[0]
    serverPort = int(args[1])
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    clientSocket.connect((serverName, serverPort))
    data = pickle.dumps([port])
    print data
    clientSocket.send(data)
    print clientSocket.recv(1024)
    addLocalRFC(port, clientSocket)
    ContactServer(port, clientSocket)
 
