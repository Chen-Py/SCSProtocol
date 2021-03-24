from rsa import *
import random

class ClientAlgo:
    
    MAXINT = 10000
    
    def __init__(self, p, q, r):
        self.RSA = RSA(p, q, r)
        self.a = None
        pass
    
    def randint(self, n):
        return random.randint(0, self.MAXINT ** n)

    def printInfo(self):
        self.RSA.printkey()
        print('a: ' + str(self.a))
        pass

    def makea(self):
        self.a = random.randint(0, self.MAXINT ** 0.5)
        return self.a

    def makeA_0(self, e, n):
        A_0 = supermy(self.a, e, n)
        return A_0

    def makeN_0(self, e, n, B_0):
        A_0 = Supermy(self.a, e, n)
        N_0 = (A_0 * B_0) % n
        return N_0
    
    def makeP(self):
        P = random.randint(0, self.MAXINT ** 0.25) * random.randint(0, self.MAXINT ** 0.25)
        return P

    def signAccept(self, s, M):
        A = supermy(a, s, M)
        return A
    
    def signRefuse(self):
        fake_a = random.randint(0, M)
        A = supermy(fake_a, s, M)
        return A

'''
client = ClientAlgo(83, 89, 97)
client.makea()
client.printInfo()
'''
