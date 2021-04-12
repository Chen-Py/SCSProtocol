from clientbase import ClientBase
from clientalgo import ClientAlgo
class SCSClient:
    def __init__(self, addr, port, siz = 1024, p =4, q = 4, e = 4):
        algo = ClientAlgo(p, q, e, siz)
        algo.printInfo()
        self.client = ClientBase(addr, port, algo)
            
    def autoSign(self, acc):
        if(self.client.sock.state != 'Connected'):
            return 'Unconnected'
        self.client.runPrepare()
        reply = self.client.sign(acc)
        print(reply)
        return reply

def dosign():
    client = SCSClient('127.0.0.1', 21567, siz = 10)
    if client.client.sock.state != 'Connected':
        print('Connection Error')
        return 'Unconnected'
    print(client.client.getContract())
    while(1):
        acc = input('Please input your attitude[Y/N]: ')
        if acc == 'Y' or acc == 'y':
            acc = True
            break
        elif acc == 'N' or acc == 'n':
            acc = False
            break
        else: print('Wrong Input!')
    return client.autoSign(acc)

dosign()
