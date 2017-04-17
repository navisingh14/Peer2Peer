import socket
import random
import thread
import pickle
import os
import glob
import platform

#Setting up UploadServer



def setupUploadServer(port):
    uploadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    uploadSocket.bind(('',port))
    uploadSocket.listen(5)
    while True:
        connectionSocket, addr = uploadSocket.accept()
        data = connectionSocket.recv(4096)
        #get the data from the rfc
        respondToRequest(connectionSocket,data)
        #connectionSocket.send(data)



def respondToRequest(connectionSocket, data):
    #check for version of p2p
    #return 505

    #check for malformation:
    #return 400
    
    filename = "RFC_"+str(rfc_num)

    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    os = platform.system()
    current_path = os.getcwd()
    if os == "Windows":
        filename = current_path + "\\rfc\\" + filename + "*"
    else:
        filename = current_path + "/rfc/" + filename + "*"
    if glob.glob(filename) == []:
        status = "404"
        phrase = "Not Found"
        request_body = "P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                    "Date:" + current_time + "\n"\
                    "OS: "+str(OS)+"\n"
        connectionSocket.send(pickle.dumps(request_body))
    else:
        status = "200"
        phrase = "OK"
        File = glob.glob(filename)
        txt = open(File[0])
        data = txt.read()
        last_modified = time.ctime(os.path.getmtime(filename))
        content_length = os.path.getsize(filename)
        request_body = ["P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                  "Date: " + current_time + "\n"\
                  "OS: " + str(OS)+"\n"\
                  "Last-Modified: " + last_modified + "\n"\
                  "Content-Length: " + str(content_length) + "\n"\
                  "Content-Type: text/text \n", str(data)]
        connectionSocket.send(pickle.dumps(request_body))      
    return message
    
    

def getUploadSocket():
    port = random.randint(7000,8000)
    return port


def get(rfc_num, rfc_title, download_host,download_port):
    os = platform.system()
    request_body = "GET RFC "+str(rfc_num)+" P2P-CI/1.0\n"\
              "Host: "+str(download_host)+"\n"\
              "OS: "+str(os)+"\n"
    downloadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    downloadSocket.connect((download_host, int(download_port)))
    downloadSocket.send(request_body)
    #get response back from client
    received_data= downloadSocket.recv(4096)
    if os == 'Windows':
        filename = os.getcwd() + "\\rfc\\RFC_"+rfc_num+"_"+rfc_title+".txt"
    else:
        filename = os.getcwd() + "/rfc/RFC_"+rfc_num+"_"+rfc_title+".txt"
    f = open(filename, 'wb')
    while(received_data):
        f.write(received_data)
        received_data = downloadSocket.recv(4096)
    f.close()
    downloadSocket.close()
    
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
                download_host = input("Enter the host name: ")
                download_port = input("Enter the port number: ")
                get(rfc_num, rfc_title, download_host, download_port)
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
'''    rfc_num = [4]
    rfc_title = ['hello']
    data= pickle.dumps([port,rfc_num, rfc_title]) 
    clientSocket.send(data)
    received_data = clientSocket.recv(4096)
    print received_data'''


if __name__ == '__main__':
    port = getUploadSocket()
    print port
    thread.start_new_thread(setupUploadServer, (port,))
    serverName = '127.0.0.1'
    serverPort = 7767
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    clientSocket.connect((serverName, serverPort))
    data = pickle.dumps([port])
    print data
    clientSocket.send(data)
    print clientSocket.recv(1024)
    addLocalRFC(port, clientSocket)
    ContactServer(port, clientSocket)
 
