from trentalgo import TrentAlgo
from socket import *
from threading import Thread, Condition

N = None
BobKey = None
AlicesA_0 = -1
AB = 1
A = -1
B = -1
P = -1
Q = -1
Contract = 'Let the room get chiller!'

class TrentBase(Thread):
    def __init__(self, clisocket, algo, actor = 'Bob'):
        Thread.__init__(self)
        self.actor = actor
        self.clisock = clisocket
        self.algo = algo
        self.algo.makes()
        self.bufsiz = 1024
        self.switch = {'hello': self.hello,
                        'CEK': self.checkconnect,
                        'PUB': self.publickey,
                        'GTK': self.getPublicKey,
                        'STB': self.sendtoBob,
                        'BGM': self.BobgetMessage,
                        'BPO': self.BobputN_0,
                        'GTA': self.getActor,
                        'GTC': self.getContract,
                        'SDC': self.sendContract,
                        'SGN': self.sign,
                        'PPM': self.prepareM
                }

    def prepareM(self):
        global P
        global Q
        print("P,Q: ", (P, Q))
        msg = self.clisock.recv(self.bufsiz).decode()
        if self.actor == 'Alice':
            P = int(msg)
            if Q != -1:
                self.algo.makeM(P, Q)
                if self.algo.M == 0:
                    P = -1
                    self.clisock.send('Retry'.encode())
                else:
                    self.clisock.send(str((self.algo.s, self.algo.M)).encode())
            else:
                self.clisock.send('Wait'.encode())

        elif self.actor == 'Bob':
            Q = int(msg)
            if P != -1:
                self.algo.makeM(P, Q)
                if self.algo.M == 0:
                    Q = -1
                    self.clisock.send('Retry'.encode())
                else:
                    self.clisock.send(str((self.algo.s, self.algo.M)).encode())
            else:
                self.clisock.send('Wait'.encode())


    def sign(self):
        msg = self.clisock.recv(self.bufsiz).decode()
        global A
        global B
        if self.actor == 'Bob':
            B = int(msg)
            if A != -1:
                if self.algo.check(A, B):
                    self.clisock.send('Succeed'.encode())
                else:
                    self.clisock.send('Failed'.encode())
            else:
                self.clisock.send('Wait'.encode())
        elif self.actor == 'Alice':
            A = int(msg)
            if B != -1:
                if self.algo.check(A, B):
                    self.clisock.send('Succeed'.encode())
                else:
                    self.clisock.send('Failed'.encode())
            else:
                self.clisock.send('Wait'.encode())


    def sendContract(self):
        global Contract
        Contract = self.clisock.recv(self.bufsiz).decode()
        self.clisock.send(Contract.encode())
        pass

    def getContract(self):
        global Contract
        self.clisock.send(Contract.encode())
        pass

    def getActor(self):
        self.clisock.send(self.actor.encode())
        pass

    def BobgetMessage(self):
        global AlicesA_0
        self.clisock.send(str(AlicesA_0).encode())

    def BobputN_0(self):
        global N
        N_0 = int(self.clisock.recv(self.bufsiz).decode())
        self.algo.makeN(N_0)

        N = self.algo.N
        self.clisock.send('True'.encode())

    def sendtoBob(self):
        global AlicesA_0
        msg = self.clisock.recv(self.bufsiz).decode()
        AlicesA_0 = int(msg)
        self.clisock.send('True'.encode())

    def getPublicKey(self):
        name = self.clisock.recv(self.bufsiz).decode()
        pubkey = None
        if name == 'Trent':
            pubkey = self.algo.RSA.public_key
        elif name == 'Bob':
            global BobKey
            pubkey = BobKey
        self.clisock.send(str((name, pubkey)).encode())


    def hello(self):
        print('HelloWorld') 

    def publickey(self):
        global BobKey
        public_key = self.clisock.recv(self.bufsiz).decode()
        public_key = tuple(public_key[1:-1].split(', '))
        public_key = int(public_key[0]), int(public_key[1])
        BobKey = public_key
        self.clisock.send(str(public_key).encode())

    def checkconnect(self):
        msg = self.clisock.recv(self.bufsiz).decode()
        print('Message: ' + msg)
        self.clisock.send('Accepted'.encode())

    def default(self):
        print(Error)
        self.clisock.send('CodeError'.encode())

    def run(self):
        while True:
            try:
                mark = self.clisock.recv(self.bufsiz).decode()
                if(mark == ''):
                    print('Logged out')
                    break
            except:
                print('Logged out')
                break
            else:
                try:
                    self.switch.get(mark, self.default)()
                except Exception as e:
                    print(e)
                    print('Logged out')
                    break
        self.clisock.close()

algo = TrentAlgo(4, 4, 4, 10)
algo.printInfo()
#algo.printInfo()
sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('127.0.0.1', 21567)) 
sock.listen(2)
print('Waiting...')
clisockBob, addrBob = sock.accept()
TBBob = TrentBase(clisockBob, algo, 'Bob')
TBBob.start()
print('...receive Bob from' + str(addrBob))

clisockAlice, addrAlice = sock.accept()
TBAlice = TrentBase(clisockAlice, algo, 'Alice')
TBAlice.start()
print('...receive Alice from' + str(addrAlice))
'''
while(1):
    clisock, addr = sock.accept()
    TB = TrentBase(clisock, algo, 'Alice')
    TB.start()
    print('...receive from' + str(addr))
'''
