from socket import *
import sys

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]')
	sys.exit(2)
	
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
server_ip = sys.argv[1] #서버 주소 입력
server_port = 1234 #포트 설정
tcpSerSock.bind((server_ip, server_port)) #서버 주소와 포트 바인딩
tcpSerSock.listen(5) #대기큐 5개
# Fill in end.
while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
	message = tcpCliSock.recv(1024).decode() #Fill / 최대 1024바이트의 요청 데이터를 받아 문자열로 변환합니다.
	print(message)
	# Extract the filename from the given message
	print(message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print(filename)
	fileExist = "false"
	filetouse = "/" + filename
	print(filetouse)

	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")                      
		outputdata = f.readlines()                        
		fileExist = "true"

		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
		tcpCliSock.send("Content-Type:text/html\r\n".encode())
		# Fill in start.
		for i in range(0, len(outputdata)):
			tcpCliSock.send(outputdata[i].encode())	#파일이 있다면 데이터를 바이트로 변환해서 클라이언트에게 모두 전송합니다.
		# Fill in end.
		print('Read from cache')

	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false": 
			# Create a socket on the proxyserver
			c = socket() #Fill / 소켓을 생성합니다.
			hostn = filename.replace("www.","",1)         
			print(hostn)   

			try:
				# Connect to the socket to port 80
				# Fill in start.
				c.connect((filename, 80)) #www.google.com과 소켓을 연결합니다.
				# Fill in end.

				# Read the response into buffer
				# Fill in start.
				c.send("GET \n".encode()) #GET 요청 데이터를 보냅니다.
				while True:
					data=c.recv(1024) #응답받은 바이트 데이터를 저장합니다.

					if not data:
						break   
						
					with open(filename, 'a') as file:
						file.write(data.decode()) #데이터를 문자열로 변환해 파일에 작성합니다.
						tcpCliSock.send(data) #데이터를 그대로 클라이언트에게 전송합니다.
				# Fill in end.

			except Exception as e:
				print("Illegal request:", e)

		else:
			# HTTP response message for file not found
			# Fill in start.
			tcpCliSock.send("HTTP/1.0 404 Not Found\r\n\r\n".encode()) #없는 경로라면 404응답 코드를 클라이언트에게 반환합니다.		
			# Fill in end.

	# Close the client and the server sockets    
	tcpCliSock.close() 

# Fill in start.
tcpSerSock.close() #소켓을 닫습니다.
# Fill in end.
