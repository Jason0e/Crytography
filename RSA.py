from random import randrange
import math

def get_prime_rounds(number):
    bit_size = number.bit_length();
    if bit_size >= 1536:
        return 3
    if bit_size >= 1024:
        return 4
    if bit_size >= 512:
        return 7
    return 10

###--------miller-rabin_test------------
def is_prime(n):
    s = n - 1
    f = s
    t = 0
    k = get_prime_rounds(n)
    if n <= 4:
        return [False, False, True, True, False][n]
    while s % 2 == 0:
        s //= 2
        t += 1
        for _ in range(k):
            a = randrange(2, f)
            v = pow(a, s, n)
            if v != 1:
                i = 0
                while v != f:
                    if i == t - 1:
                        return False
                    else:
                        i += 1
                        v = (v ** 2) % n
        return True
    return False


##---------按十进制长度生成素数-------------
def get_large_prime_length(length=500):
    size = 10 ** length
    n = 10 ** (length - 1)
    while True:
        num = randrange(n, size)
        if is_prime(num):
            return num

def prime_range(start, end):
    sieve = [True] * end
    primes = []
    sieve[0] = False
    sieve[1] = False
    for i in range(2, int(math.sqrt(end)) + 1):
        point = i * 2
        while point < start:
            point += i
        while point < end:
            sieve[point] = False
            point += i

    for i in range(start, end):
        if sieve[i]:
            primes.append(i)
    return primes

###----------按bit位数生成素数--------------
def get_large_prime_bit_size(bit_size=512):
    size = 2 ** bit_size
    n = 2 ** (bit_size - 1)
    while True:
        num = randrange(n, size)
        if is_prime(num):
            return num


# 最大公约数
def gcd(a, b):
    while b != 0:
        tmp = a % b
        a = b
        b = tmp
    return a


# 扩展欧几里得
def ex_gcd(a, b, arr):
    if b == 0:
        arr[0] = 1
        arr[1] = 0
        return a
    g = ex_gcd(b, a % b, arr)
    t = arr[0]
    arr[0] = arr[1]
    arr[1] = t - int(a / b) * arr[1]
    return g


# 求逆元
def Modreverse(a, n):
    arr = [0, 1, ]
    gcd = ex_gcd(a, n, arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
    else:
        return -1

def encrypt(m, c, n, e):
    for i in range(len(m)):
        if m[i] != ' ':
            c.append(chr((pow(ord(m[i]),e)%n)%26+65))
        else:
            c.append(' ')
    d = ''.join(c)
    print(d)

def decrypt(c, dec_m, n, d):
    for i in range(len(c)):
        if c[i] != ' ':
            dec_m.append(chr((pow(ord(c[i]),d)%n)%26+97))
        else:
            dec_m.append(' ')
    p = ''.join(dec_m)
    print(p)

if __name__ == "__main__":
    plaintext = input("请输入明文：")
    c = []
    dec_m = []
    bsize = 32
    bsize = int(input("输入需要的大素数长度(bits)："))
    #获得大素数
    p = get_large_prime_bit_size(bsize)
    q = p
    while(q==p):
        q = get_large_prime_bit_size(bsize)
    #获得n
    print("p:",p)
    print("q:",q)
    n = (p-1)*(q-1)
    print("n",n)
    #获得e
    e = n
    while(gcd(e,n)!=1):
        e = randrange(2,n)
    print("e",e)
    #获得d
    d = Modreverse(e,n)
    print("d",d)
    encrypt(plaintext,c,n,e)
    decrypt(c,dec_m,n,d)
    #加密
    # print("m:",plaintext)
    # c = pow(plaintext,e)%n
    # print(c)
    # #解密
    # dec_m = pow(c,d)%n
    # print(dec_m)
    pass