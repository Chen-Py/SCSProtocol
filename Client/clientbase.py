from clientalgo import ClientAlgo
from clientsocket import TcpCliSock

class ClientBase:

    def __init__(self, host, port, algo):
        self.algo = algo
        self.bufsiz = 1024
        self.sock = TcpCliSock(host, port, self.bufsiz)

    def checkconnect(self):
        self.sock.send('CEK', 'Hello,Trent')
        print(self.sock.recvstr())
        pass
    
    def publicRSAkey(self):
        self.sock.send('PUB', str(self.algo.RSA.public_key).encode())
        reply = self.sock.recvstr()
        if(reply == str(self.algo.RSA.public_key)):
            return True
        else:
            return False



algo = ClientAlgo(23, 29, 31)
client = ClientBase('127.0.0.1', 21567, algo)

print(client.sock.state)
print(client.publicRSAkey())
