from trentalgo import TrentAlgo
from socket import *
from threading import Thread

class TrentBase(Thread):
    def __init__(self, clisocket, algo):
        Thread.__init__(self)
        self.clisock = clisocket
        self.algo = algo
        self.bufsiz = 1024
        self.switch = {'hello': self.hello,
                        'CEK': self.checkconnect,
                        'PUB': self.publickey,
                        'GTK': self.getPublicKey,
                        'STB': self.sendtoBob
                }

    def sendtoBob(self):
        msg = self.clisock.recv(self.bufsiz).decode()
        self.clisock.send('True'.encode())

    def getPublicKey(self):
        name = self.clisock.recv(self.bufsiz).decode()
        self.clisock.send(str(('Chen_Py', (123, 456))).encode())


    def hello(self):
        print('HelloWorld') 

    def publickey(self):
        public_key = self.clisock.recv(self.bufsiz).decode()
        public_key = tuple(public_key[1:-1].split(', '))
        public_key = int(public_key[0]), int(public_key[1])
        self.clisock.send(str(public_key).encode())

    def checkconnect(self):
        msg = self.clisock.recv(self.bufsiz).decode()
        print('Message: ' + msg)
        self.clisock.send('Accepted'.encode())

    def default(self):
        print(Error)
        self.clisock.sed('CodeError'.encode())

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
                except:
                    print('Logged out')
                    break
        self.clisock.close()
algo = TrentAlgo(83, 89, 97)
sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('127.0.0.1', 21567)) 
sock.listen(5)
print('Waiting...')
while(1):
    clisock, addr = sock.accept()
    TB = TrentBase(clisock, algo)
    TB.start()
    print('...receive from' + str(addr))
