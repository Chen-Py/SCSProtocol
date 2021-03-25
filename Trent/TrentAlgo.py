from rsa import *
import random
class TrentAlgo:
    
    MAXINT = 10000

    def __init__(self, p, q, e):
        self.RSA = RSA(p, q, e)
        self.N = None
        self.s = None
        self.M = None
        pass

    def printInfo(self):
        self.RSA.printkey()
        print('N: ' + str(self.N))
        print('s: ' + str(self.s))
        print('M: ' + str(self.M))
        pass
    
    def makeN(self, N_0):
        self.N = self.RSA.decode(N_0)
        return self.N

    def makeM(self, P, Q):
        self.M = P * Q
        return self.M

    def makes(self):
        self.s = random.randint(1, self.MAXINT)
        return self.s

    def check(self, A, B):
        return (A * B) % self.M == supermy(self.N, self.s, self.M)


'''
trent = TrentAlgo(83, 89, 97)
trent.makeN(trent.RSA.encode(1024))
trent.makeM(2, 3)
trent.makes()
trent.printInfo()
'''
