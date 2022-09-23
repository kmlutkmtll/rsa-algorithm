import random
from math import floor
from math import sqrt

RANDOM_START = 100
RANDOM_END = 150

number = random.randint(1,100)

def is_prime(num):
    # numbers smaller than 2 can not be primes
    if num < 2:
        return False

    # this is the only even prime number
    if num == 2:
        return True

    # even numbers can not be primes
    if num % 2 == 0:
        return False

    # we have already checked numbers < 3
    # finding primes up to N we just have to check numbers up to sqrt(N)
    # increment by 2 because we have already considered even numbers
    for i in range(3, floor(sqrt(num))):
        if num % i == 0:
            return False

    return True

# Euclid's greatest common divisor algorithm: this is how we can verify
# whether (e,phi) are coprime ... with the gcd(e,phi)=1 condition
def gcd(a, b):

    while b != 0:
        a, b = b, a % b

    return a

# extended Euclid's algorithm to find modular inverse in O(log m) so in linear time
# this is how we can find the d value which is the modular inverse of e in the RSA cryptosystem
def modular_inverse(a, b):

    # of course because gcd(0,b)=b and a*x+b*y=b - so x=0 and y=1
    if a == 0:
        return b, 0, 1

    # so we use the Euclidean algorithm for gcd()
    # b%a is always the smaller number - and 'a' is the smaller integer always in this implementation
    div, x1, y1 = modular_inverse(b % a, a)

    # and we update the parameters for x, y accordingly
    x = y1 - (b // a) * x1
    y = x1

    # we use recursion so this is how we send the result to the previous stack frame
    return div, x, y

def generate_large_prime(start=RANDOM_START, end=RANDOM_END):
    # generate a random number [RANDOM_START,RANDOM_END]
    num = random.randint(start, end)

    # and check whether it is prime or not
    while not is_prime(num):
        num = random.randint(start, end)

    # we know the number is prime
    return num

"""
if ((is_prime(p) == False) or (is_prime(q) == False)):
    while(is_prime(p) == False or is_prime(q) == False):
        p = int(input("Please enter a big prime number(100-150) : "))
        q = int(input("Please enter a big prime number(100-150) : "))
"""


def generate_RSA_keys():
    # generate the first huge random prime number
    p = generate_large_prime()
    print("p : ",p)
    # generate the second huge random prime number
    q = generate_large_prime()
    print("q : ",q)

    # this is the trapdoor function: multiplying is fast but getting p and q
    # from n is an exponentially slow operation

    n = p * q

    # Euler's totient phi function
    phi = (p-1)*(q-1)

    e = random.randrange(1, phi)

    # we must make sure gcd(e,phi)=1 so e and phi are coprime
    # otherwise we cannot find d
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)


    # d is the modular inverse of e
    d = modular_inverse(e, phi)[1]

    # private key and the public key
    return (d, n), (e, n)



def encrypt(public_key):
    # e and n are needed for encryption (these are public!!!)
    e, n = public_key
    a = pow(number,e,n)
    return a


# decrypt messages: we use private keys for decryption
def decrypt(private_key):
    # d and n are needed for decryption (these are private!!!)
    d, n = private_key

    enc = encrypt(public_key)
    a = pow(enc,d,n)
    return a

private_key, public_key = generate_RSA_keys()

print("Public key : ",public_key)
print("Private key : ",private_key)

print("Original message: %d" % number)
encrypted = encrypt(public_key)
print("Encrypted: %d" % encrypted)
decrypted = decrypt(private_key)
print("Decrypted text: %d" % decrypted)




