from clientalgo import ClientAlgo
from clientsocket import TcpCliSock
import time


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

    def getPublicKey(self, name):
        self.sock.send('GTK', name)
        reply = self.sock.recvstr()
        try:
            tmp = reply[1: -1].split(', (')
            name = tmp[0][1: -1]
            public_key = tmp[1][0:-1].split(', ')
            public_key = int(public_key[0]), int(public_key[1])
        except:
            return 1,(1,1)
        return name, public_key

    def sendtoBob(self, msg):
        self.sock.send('STB', str(msg))
        reply = self.sock.recvstr()
        return bool(reply)

    def prepareAlice(self):
        self.algo.makea()
        name, public_key = self.getPublicKey('Trent')
        A_0 = self.algo.makeA_0(public_key[0], public_key[1])
        while(1):
            name, public_key = self.getPublicKey('Bob')
            if public_key != (1,1):break
            print("Waiting for Bob...")
            time.sleep(2)
        sA_0 = self.algo.RSA.docode(A_0, public_key)
        return self.sendtoBob(sA_0)
#
    def Bobgetmsg(self):
        self.sock.send('BGM', None)
        reply = self.sock.recvstr()
        try:
            return int(reply)
        except:
            return 0
#
    def BobputN_0(self, N_0):
        self.sock.send('BPO', str(N_0))
        reply = self.sock.recvstr()
        return bool(reply)

    def prepareBob(self):
        self.algo.makea()
        self.publicRSAkey()
        name, public_key = self.getPublicKey('Trent')
        B_0 = self.algo.makeA_0(public_key[0], public_key[1])
        while(1):
            sA_0 = self.Bobgetmsg()
            if(int(sA_0) != 0):break
            print("Waiting for Alice...")
            time.sleep(2)
        A_0 = self.algo.RSA.decode(sA_0)
        N_0 = (A_0 * B_0) % public_key[1]
        return self.BobputN_0(N_0)





algo = ClientAlgo(173, 179, 181)
client = ClientBase('127.0.0.1', 21567, algo)
client.algo.printInfo()
print(client.publicRSAkey())
client.prepareAlice()
print('a: ' + str(client.algo.a))

print('As Bob: ')
print(client.Bobgetmsg())

print(client.prepareBob())
print('b: ' + str(client.algo.a))
'''
print(client.sock.state)
print(client.getPublicKey('Bob'))
print(client.getPublicKey('Trent'))
client.sendtoBob('123')
'''
