import socket
import random
import thread
import pickle

#Setting up UploadServer



def setupUploadServer(port):
    uploadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    uploadSocket.bind(('',port))
    uploadSocket.listen(5)
    while True:
        connectionSocket, addr = uploadSocket.accept()
        RFC = connectionSocket.recv(4096)
        #get the data from the rfc
        #connectionSocket.send(data)
        
    

def getUploadSocket():
    port = random.randint(7000,8000)
    return port


def add():
    request_body = "ADD RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(rfc_title)+"\n"
    return request_body

def lookup(rfc_num, rfc_title):
    request_body = "LOOKUP RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(rfc_title)+"\n"
    return request_body

def list_rfc():
    request_body = "LIST ALL P2P-CI/1.0 \n"\
              "Host: "+str(host)+"\n"\
              "Port: "+str(port)+"\n"
    return request_body


#Contacting Server
def ContactServer(port, clientSocket):
    user_input = raw_input("> Enter the command: ADD, LIST, LOOKUP, GET, EXIT")
    if user_input == 'ADD':
        data = pickle.dumps(list_rfc())
        clientSocket.send(data)
        ContactServer(port, clientSocket)
    elif user_input == 'LIST':
        data = pickle.dumps(list_rfc())
        clientSocket.send(data)
        ContactServer(port, clientSocket)
    elif user_input == 'LOOKUP':
        rfc_num = input("Enter the RFC number: ")
        rfc_title = raw_input("Enter the RFC title: ")
        data = pickle.dumps(lookup(rfc_num, rfc_title))
        clientSocket.send(data)
        ContactServer(port, clientSocket)
    elif user_input == 'GET':
        ContactServer(port, clientSocket)
    elif user_input == 'EXIT':
        clientSocket.close()
'''    rfc_num = [4]
    rfc_title = ['hello']
    data= pickle.dumps([port,rfc_num, rfc_title]) 
    clientSocket.send(data)
    received_data = clientSocket.recv(4096)
    print received_data'''


print socket.gethostname();


if __name__ == '__main__':
    port = getUploadSocket()
    print port
    thread.start_new_thread(setupUploadServer, (port,))
    serverName = '127.0.0.1'
    serverPort = 7767
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    clientSocket.connect((serverName, serverPort))
    ContactServer(port, clientSocket)
 
