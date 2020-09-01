# Some simple algorithms for modular arithmetic!

import random

## Keys will be of size 100
N_BITS-100


def random_integer(start=None, end=None):
    if start is None: start = 2**(N_BITS-2)
    if end is None: end = 2**(N_BITS)
    return random.randint(start,end)


def gcd(x,y):
    # Euclid's algorithm!
    # INPUT: integers x,y >= 0
    # OUTPUT: d = gcd(x,y) 
    
    if y==0: return x
    else: return gcd(y, x % y)

def gcdplus(x,y):
    # Extended-Euclid's algorithm!
    # INPUT: integers x,y
    # OUTPUT: d,a,b where 
    #         -- d = gcd(x,y),
    #         -- d = a*x + b*y
    
    if x < y:
        d,a,b = gcdplus(y,x)
        return d,b,a
    
    if y == 0: return x,1,0
    
    d_, a_, b_ = gcdplus(y, x % y)
    
    return d_, b_, a_ - (x//y) * b_


def modexp(x,y,N):
    # INPUT: integers x,y >= 0, N > 0
    # OUTPUT: x^y mod N

    if y==0: return 1

    z = modexp(x,y // 2,N)

    if y % 2 == 0: return z*z % N
    else: return x*z*z % N

    
def mult_inverse_mod(x,N):
    # INPUT: integer x, modulus N > 0
    if gcd(x,N) != 1:
        raise ValueError('gcd(%d,%d)=/=1'%(x,N))
    d,a,b = gcdplus(x,N)
    return a % N

def fermat_prime_test(X, numiter=30):
    # INPUT: integer X
    # OUTPUT: True/False if X is prime
        
    for iter in range(numiter):
        a = random_integer(2,X-1)
        fermat_check = modexp(a,X-1,X)
        if  fermat_check != 1: return False
        
    return True 

def randomprime(numbits):
    # INPUT: numbits
    # OUTPUT: a random prime X of size roughly numbits
    
    while True:

        X = random_integer(numbits)
        
        if fermat_prime_test(X): return X


def keygen(n_bits=128):

    P = randomprime(n_bits)
    Q = randomprime(n_bits)
    
    expon = 2 # This is just a default value
    while gcd(expon,(P-1)*(Q-1)) != 1:
        # try random expon until  gcd(expon,(P-1)*(Q-1))=1
        expon = random_integer(n_bits)
        
    expon_inv = mult_inverse_mod(expon,(P-1)*(Q-1))
    
    print("==PUBLIC KEY==\nPQ=%d\nexpon=%d\n"%(P*Q,expon))
    print("==PRIVATE KEY==\nP=%d\nQ=%d\nexpon_inv=%d" % (
        P,Q,expon_inv))
    return P,Q,expon,expon_inv

def rsa_encrypt_int(message,expon,PQ):
    # Computes message^expon mod PQ
    return modexp(message,expon,PQ)

def rsa_decrypt_int(encrypted,expon_inv,PQ):
    # Computes encrypted^expon_inv mod PQ
    return modexp(encrypted,expon_inv,PQ)


def test_rsa_works(message=111112222233333, P,Q,expon,expon_inv):
    print("The plaintext message is %d" % message)
    print("We are now going to encrypt this message using the public key")
    print("The public key is:")
    print("PQ = %d" % (P*Q))
    print("expon=%d"%expon)
    encrypted= rsa_encrypt_int(plaintext,expon,P*Q)
    print("The encrypted message is %d" % encrypted)
    decrypted = rsa_decrypt_int(encrypted_text,expon_inv,P*Q)
    print("The decrypted message is %d"% decrypted)
    works = decrypted == message
    if works:
        print("RSA protocol worked!")
    else: print("Hmmm for some reason the RSA protocol failed")


if __name__ == '__main__':
    P,Q,expon,expon_inv = keygen(N_BITS)
    test_rsa_works
    
    test_rsa_works

