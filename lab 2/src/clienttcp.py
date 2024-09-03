from socket import *
import threading

def sendmsg(sendSocket):
    while True:
        msg = input()
        if ((msg[0] !='@') and ('All' not in msg)) or (' ' not in msg) :
            print('Enter Correct String ')
            continue
        [user, data] = msg.split(' ',1)
        if ('All' not in user):
            user = user.split('@')[1]
        i = 0
        while i<len(user):
            if (ord(user[i]) < 65 or ord(user[i]) > 90) and (ord(user[i]) < 97 or ord(user[i]) > 122) and (ord(user[i]) < 48 or ord(user[i]) > 57):
                print('Enter Correct String ')
                break
            i = i+1
        if i<len(user):
            continue
        msg = 'SEND '+ user + '\n' + 'Content-length: ' + str(len(data)) + '\n' + '\n' + data
        #msg = 'SEND '+ user + '\n' + 'Content-length: ' + str(0) + '\n' + '\n' + data
        sendSocket.send(msg.encode())
        res = sendSocket.recv(1024).decode()
        if 'SEND' in res:
            print('Message Delivered successfully\n')
        elif 'ERROR 102' in res:
            print('Unable to send\n')
        else:
            print('Header Incomplete\n')

def recvmsg(recvSocket):
    while True:
        res = recvSocket.recv(1024).decode()
        if len(res.split('\n')) != 4:
            msg = 'ERROR 103 Header Incomplete\n\n'
            recvSocket.send(msg.encode())
            recvSocket.close()
            break
        msg = res.split('\n')
        if (len(msg[0].split(' ')) != 2) or (msg[0].split(' ')[0] != 'FORWARD'):
            msg = 'ERROR 103 Header Incomplete\n\n'
            recvSocket.send(msg.encode())
            recvSocket.close()
            break
        if (len(msg[1].split(' ')) != 2) or (msg[1].split(' ')[0] != 'Content-length:'):
            msg = 'ERROR 103 Header Incomplete\n\n'
            recvSocket.send(msg.encode())
            recvSocket.close()
            break
        if (int(msg[1].split(' ')[1]) < len(msg[3])):
            msg = 'ERROR 103 Header Incomplete\n\n'
            recvSocket.send(msg.encode())
            recvSocket.close()
            break
        print(msg[3])
        msg = 'RECEIVED ' + msg[0].split(' ')[1] + '\n' + '\n'
        recvSocket.send(msg.encode())

while True:
    user = input('Enter username ')
    i=0
    while i<len(user):
        if (ord(user[i]) < 65 or ord(user[i]) > 90) and (ord(user[i]) < 97 or ord(user[i]) > 122) and (ord(user[i]) < 48 or ord(user[i]) > 57):
            print('Provide correct username please!')
            break
        i = i+1
    if i == len(user):
        break

serverName = input('Enter server IP ')
serverPort = 12000

recvSocket = socket(AF_INET,SOCK_STREAM)
recvSocket.connect((serverName,serverPort))
sendSocket = socket(AF_INET,SOCK_STREAM)
sendSocket.connect((serverName,serverPort))


msg = 'REGISTER TORECV '+ user + '\n \n'
recvSocket.send(msg.encode())
res = recvSocket.recv(1024).decode()
if 'ERROR 100' in res:
    print('Enter correct username')
elif 'REGISTERED' not in res:
    print('Register the user first1')

msg = 'REGISTER TOSEND '+ user + '\n \n'
sendSocket.send(msg.encode())
res = sendSocket.recv(1024).decode()
if 'ERROR 100' in res:
    print('Enter correct username')
elif 'REGISTERED' not in res:
    print('Register the user first2')
else:
    t2 = threading.Thread(target = recvmsg, args = [recvSocket])
    t2.start()
    t1 = threading.Thread(target = sendmsg, args = [sendSocket])
    t1.start()
