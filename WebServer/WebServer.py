#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverPort = 1234  #포트 번호를 설정합니다.
serverSocket.bind(('', serverPort))
serverSocket.listen(1)  #소켓 대기큐의 크기를 설정합니다.
#Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr =  serverSocket.accept() #Fill / 소켓을 열어두고 블락되어 데이터가 오면 수신합니다.
    try:
        message = connectionSocket.recv(1024).decode() #Fill / 최대 1024바이트의 데이터를 받아와 문자열로 디코딩합니다.              
        filename = message.split()[1]                 
        f = open(filename[1:])                        
        outputdata = f.read() #Fill / 지정된 파일의 데이터를 읽어와 저장합니다.
        #Send one HTTP header line into socket
        #Fill in start
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())   #응답코드를 전송합니다.
        #Fill in end                
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        #Fill in start   
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode()) 
        #해당 위치에 파일의 데이터가 없어 예외가 발생하면 404응답 코드를 반환합니다.    
        #Fill in end
        
        #Close client socket
        #Fill in start
        connectionSocket.close() #연결 소켓을 닫습니다.
        #Fill in end            
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data  