from socket import *
import threading

table ={}

def func(connSocket):
    msg = connSocket.recv(1024).decode()
    if 'REGISTER TORECV' in msg:
        user = msg.split('\n')[0].split(' ')[2]
        i = 0
        while i<len(user):
            if (ord(user[i]) < 65 or ord(user[i]) > 90) and (ord(user[i]) < 97 or ord(user[i]) > 122) and (ord(user[i]) < 48 or ord(user[i]) > 57):
                msg = 'ERROR 100 Malformed username\n \n'
                connSocket.send(msg.encode())
                break
            i = i+1
        if i == len(user):
            msg = 'REGISTERED TORECV ' + user + '\n \n'
            table[user] = connSocket
            print(table)
            connSocket.send(msg.encode())
    else:
        user = msg.split('\n')[0].split(' ')[2]
        i = 0
        if user not in table:
            msg = 'ERROR 101 No user registered\n \n'
            connSocket.send(msg.encode())
        else:
            while i<len(user):
                if (ord(user[i]) < 65 or ord(user[i]) > 90) and (ord(user[i]) < 97 or ord(user[i]) > 122) and (ord(user[i]) < 48 or ord(user[i]) > 57):
                    msg = 'ERROR 100 Malformed username\n \n'
                    connSocket.send(msg.encode())
                    break
                i = i+1
            if i == len(user):
                msg = 'REGISTERED TOSEND ' + user + '\n \n'
                connSocket.send(msg.encode())
                while True:
                    res = connSocket.recv(1024).decode()
                    if len(res.split('\n')) != 4:
                        msg = 'ERROR 103 Header Incomplete\n\n'
                        connSocket.send(msg.encode())
                        connSocket.close()
                        break
                    msg = res.split('\n')
                    if (len(msg[0].split(' ')) != 2) or (msg[0].split(' ')[0] != 'SEND'):
                        msg = 'ERROR 103 Header Incomplete\n\n'
                        connSocket.send(msg.encode())
                        connSocket.close()
                        break
                    if (len(msg[1].split(' ')) != 2) or (msg[1].split(' ')[0] != 'Content-length:'):
                        msg = 'ERROR 103 Header Incomplete\n\n'
                        connSocket.send(msg.encode())
                        connSocket.close()
                        break
                    if (int(msg[1].split(' ')[1]) < len(msg[3])):
                        msg = 'ERROR 103 Header Incomplete\n\n'
                        connSocket.send(msg.encode())
                        connSocket.close()
                        break
                    recipient = msg[0].split(' ')[1]
                    flag = False
                    if recipient == 'All':
                        for k in table.keys():
                            if k == user:
                                continue
                            forward = 'FORWARD ' + user + '\n' + 'Content-length: ' + msg[1].split(' ')[1] + '\n\n' + msg[3]
                            try:
                                table[k].send(forward.encode())
                                res_recipient = table[k].recv(1024).decode()
                            except:
                                flag = False
                                break
                            if 'RECEIVED' in res_recipient:
                                flag = True
                            else:
                                if 'ERROR 103' in res_recipient:
                                    table[k].close()
                                    del table[k]
                                    print(table)
                                flag = False
                                break
                        if flag == True:
                            msg1 = 'SEND ' + recipient + '\n\n'
                            connSocket.send(msg1.encode())
                        else:
                            msg1 = 'ERROR 102 Unable to send\n\n'
                            connSocket.send(msg1.encode())
                    elif recipient not in table.keys():
                        msg = 'ERROR 102 Unable to send\n\n'
                        connSocket.send(msg.encode())
                        continue
                    else:
                        forward = 'FORWARD ' + user + '\n' + 'Content-length: ' + msg[1].split(' ')[1] + '\n\n' + msg[3]
                        try:
                            table[recipient].send(forward.encode())
                            res_recipient = table[recipient].recv(1024).decode()
                            if 'RECEIVED' in res_recipient:
                                msg = 'SEND ' + recipient + '\n\n'
                                connSocket.send(msg.encode())
                            else:
                                if 'ERROR 103' in res_recipient:
                                    table[recipient].close()
                                    del table[recipient]
                                    print(table)
                                msg = 'ERROR 102 Unable to send\n\n'
                                connSocket.send(msg.encode())
                        except:
                            msg = 'ERROR 102 Unable to send\n\n'
                            connSocket.send(msg.encode())


serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

while True:
    connSocket, clientaddr = serverSocket.accept()
    t = threading.Thread(target = func , args = [connSocket])
    t.start()
