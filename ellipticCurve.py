import math
 
def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: 
            return False
    return True

def power(x, exponent, primeMod):
    # power finder only if mod prime
    if exponent == 0: return 1
    p = power(x, exponent//2, primeMod) % primeMod
    p = (p * p) % primeMod

    if (exponent % 2) == 0: return p 
    else: return (x * p % primeMod)

def gcd(a, b):
    if (a == 0): return b
    return gcd(b % a, a)

def moduloInverse(x, primeMod):
    greatestCommonDivisor = gcd(x, primeMod)
    if (greatestCommonDivisor != 1): print("Inverse non-existent")
    else: return power(x, primeMod-2, primeMod)

def yExist(y, mod):
    for i in range(1, mod):
        if (i * i) % mod == y: return i
        else: return -1

class EllipticCurve():

    def __init__(self, a, b, prime):
        # y^2 = x^3 + ax + b mod prime
        self.a = a % prime
        self.b = b % prime
        self.prime = prime
        self.o = (0,0) # point not on curve i.e. inf
 
    def validityCheck(self):
        valid = True
        # Check discriminant
        if (4 * (self.a ** 3) + 27 * (self.b ** 2))  % self.prime == 0: valid = False
        # Check primality 
        if not is_prime(self.prime): valid = False
        return valid

    def add(self, point1, point2):
        # Case: P + O = P = O + P
        if point1 == self.o: return point2
        if point2 == self.o: return point1

        # Case: P + Q = O
        if point1[0] == point2[0] and point1[1] != point2[1]: return self.o

        # Case: P + P = R
        if point1[0] == point2[0]:
            gradient = (3 * point1[0] * point1[0] + self.a) * moduloInverse((2 * point1[1]) % self.prime, self.prime) % self.prime

        # Case: P + Q = R
        else:
            gradient = (point2[1] - point1[1]) * moduloInverse((point2[0] - point1[0]) % self.prime, self.prime) % self.prime
        x = ((gradient * gradient) - point1[0] - point2[0]) % self.prime
        y = (gradient * (x - point1[0]) + point1[1]) % self.prime
        return (x,-y % self.prime)
    
    def findAllPoints(self):
        allPoints = list()
        for x in range(0,self.prime):
            for y in range(0,self.prime):
                # Check if y^2=x^3 + Ax + B for all values up to modulus.
                if (y * y) % self.prime == ((x * x * x) + self.a*x + self.b) % self.prime:
                    # If equal add to list
                    allPoints.append((x,y))

        # Also add point at inf.
        allPoints.append(self.o)

        return allPoints 

    def findOrder(self, point):
        # If point is self inverse, order = 1
        if point == self.o: return 1
        
        # If y-coord is 0, by def order = 2
        if point[1] == 0: return 2

        # Order 1 and 2 complete. 
        counter = 2
        output = point
        while True:
            # Add point to itself until equals identity. Number of additions is the order of that point.
            output = self.add(point,output)
            if output == self.o: return counter
            counter += 1

    def findAllOrder(self):
        # Make list of all points
        allPoints = self.findAllPoints()
        orderArray = list()

        # Assign order of each point in list using findOrder()
        for point in allPoints:
            orderArray.append(self.findOrder(point))
        
        orderArray.sort()
        return orderArray




