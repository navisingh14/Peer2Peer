from socket import *
import random
import pickle

serverName = '127.0.0.1'
serverPort = 7754
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

port = random.randint(8000,9000)
rfc_num = 4
rfc_title = 'hello'
data= pickle.dumps([port,rfc_num, rfc_title])

clientSocket.send(data)
modifiedSentence = clientSocket.recv(1024)
print 'From Server:', modifiedSentence
clientSocket.close()
