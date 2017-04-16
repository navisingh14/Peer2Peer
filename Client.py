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
        respondToRequest(connectionSocket,data):
        #connectionSocket.send(data)



def respondToRequest(connectionSocket, data):
    #check for version of p2p
    #return 505

    #check for malformation:
    #return 400
    
    filename = "rfc"+str(rfc_num)+".txt"

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


def get(rfc_num, rfc_title, download_host):
    os = platform.system()
    request_body = "GET RFC "+str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: "+str(download_host)+"\n"\
              "OS: "+str(os)+"\n"
    downloadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    downloadSocket.connect((download_host, int(download_port)))
    downloadSocket.send(request_body)
    #get response back from client
    #received_data= pickle.loads(downloadSocket.recv(4096)
    if os == 'Windows':
        filename = os.getcwd() + "\\rfc\\RFC_"+rfc_num+"_"+rfc_title+".txt"
    else:
        filename = os.getcwd() + "/rfc/RFC_"+rfc_num+"_"+rfc_title+".txt"
    with open(filename, 'w') as f:
        f.write(received_data)
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







def add(clientSocket, rfc_num, rfc_title):
    request_body = "ADD RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(rfc_title)+"\n"
    data = pickle.dumps(request_body)
    clientSocket.send(data)
    idata1 = clientSocket.recv(1024)
    idata2 = clientSocket.recv(1024)
    print idata1
    print idata2    

def lookup(clientSocket, rfc_num, rfc_title):
    request_body = "LOOKUP RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(rfc_title)+"\n"
    data = pickle.dumps(lookup(rfc_num, rfc_title))
    clientSocket.send(data)
    available_peers = pickle.loads(clientSocket.recv(4096))

def list_rfc(clientSocket):
    request_body = "LIST ALL P2P-CI/1.0 \n"\
              "Host: "+str(host)+"\n"\
              "Port: "+str(port)+"\n"
    data = pickle.dumps(request_body)
    clientSocket.send(data)


#Contacting Server
def ContactServer(port, clientSocket):
    try:
        user_input = raw_input("> Enter the command: ADD, LIST, LOOKUP, EXIT:\n")
        if user_input == 'ADD':
            cwd = os.getcwd();
            if platform.system() == 'Windows':
                print "List of available RFCs on local system"
                for each_rfc in glob.glob(cwd + "\\rfc\\*.pdf"):
                    print each_rfc
            else:
                print "List of available RFCs on local system"
                for each_rfc in glob.glob(cwd + "/rfc/*.pdf"):
                    print each_rfc
            rfc_num = input("Enter the RFC number: ")
            rfc_title = raw_input("Enter the RFC title: ")
            add(clientSocket, rfc_num, rfc_title)
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
 
