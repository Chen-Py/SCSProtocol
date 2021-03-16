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

    def getPublicKey(self, name):
        self.sock.send('GTK', name)
        reply = self.sock.recvstr()
        tmp = reply[1: -1].split(', (')
        name = tmp[0][1: -1]
        public_key = tmp[1][0:-1].split(', ')
        public_key = int(public_key[0]), int(public_key[1])
        return name, public_key

    def sendtoBob(self, msg):
        self.sock.send('STB', msg)
        reply = self.sock.recvstr()
        return bool(reply)

    def prepareAlice(self):
        self.algo.makea()
        name, public_key = self.getPublicKey('Trent')
        A_0 = self.algo.makeA_0(public_key[0], public_key[1])
        time.sleep(1)
        name, public_key = self.getPublicKey('Bob')
        if public_key == None:return None
        sA_0 = self.algo.RSA.docode(A_0, public_key)
        time.sleep(0.1)
        return self.sendtoBob(sA_0)
#
    def Bobgetmsg(self):
        self.sock.send('BGM', None)
        reply = self.sock.recvstr()
        return int(reply)
#
    def BobputN_0(self, N_0):
        self.sock.send('BPO', str(N_0))
        reply = self.sock.recvstr()
        return bool(reply)

    def prepareBob(self):
        self.algo.makea()
        self.publicRSAkey()
        time.sleep(0.1)
        name, public_key = self.getPublicKey('Trent')
        B_0 = self.algo.makeA_0(public_key[0], public_key[1])
        time.sleep(2)
        sA_0 = self.Bobgetmsg()
        A_0 = self.algo.RSA.decode(sA_0)
        N_0 = (A_0 * B_0) % public_key[1]
        time.sleep(0.1)
        return self.BobputN_0(N_0)





algo = ClientAlgo(23, 29, 31)
client = ClientBase('127.0.0.1', 21567, algo)

print(client.sock.state)
print(client.publicRSAkey())
print(client.getPublicKey('Bob'))
client.sendtoBob('123')
print(client.Bobgetmsg())
