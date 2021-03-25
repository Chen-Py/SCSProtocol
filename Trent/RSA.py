def supermy(a, n, m):
    if n == 0:return 1
    if n % 2 == 1:return (a * supermy(a, n-1, m)) % m
    tmp = supermy(a, n/2, m)
    return (tmp * tmp) % m

def gcd(a, b):
    if b == 0:return a
    return gcd(b, a % b)

def exgcd(a, b):
    if b == 0:
        return 1, 0
    else:
        x1, y1 = exgcd(b, a % b)
        x, y = y1, x1 - (a // b) * y1
    return x, y

def inv(e, phi):
    if(gcd(e, phi)!=1):return None
    x, y = exgcd(e, phi)
    ans = x % (abs(phi))
    return ans

class RSA:

    def __init__(self, p, q, e):
        self.makekey(p, q, e)
        pass

    def printkey(self):
        print('Private Key: ' + str(self.private_key))
        print('Public Key: ' + str(self.public_key))

    def makekey(self, p, q, e):
        n = p * q
        phi = (p - 1) * (q - 1)
        if gcd(e, phi) != 1:return None
        d = inv(e, phi)
        self.public_key = (e, n)
        self.private_key = (d, n)
        return self.public_key, self.private_key

    def encode(self, m):
        if self.public_key == None:return None
        c = supermy(m, self.public_key[0], self.public_key[1])
        return c

    def decode(self, c):
        if self.private_key == None:return None
        m = supermy(c, self.private_key[0], self.private_key[1])
        return m

    def docode(self, msg, key):
        ans = supermy(msg, key[0], key[1])
        return ans

    pass

