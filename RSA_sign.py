import math
import random
import sys
import io
from hashlib import sha1

# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


plainText = ''
cipherText = ''
Digest = ''
ps_key = ()

PLAIN_TEXT_FILE = "test.txt"     #明文文件
SECRET_KEY_FILE = "secretKey.txt"     #密钥文件

RECEIVED_TEXT_FILE = "test1.txt"    #接收到的消息文件


def ascll2bit(str_in, num):  # 字符转二进制,补齐到num位
    m = str_in
    bit_text = ''
    for i in m:
        tmp = str(bin(ord(i))).replace('0b', '')
        while len(tmp) % num != 0:
            tmp = '0' + tmp
        bit_text += tmp
    return bit_text


def quickPower(a, b, c):
    result = 1
    while b > 0:
        if b & 1:
            result = result * a % c
        a = a * a % c
        b >>= 1
    return result


def miller_rabin(n):  # Miller Rabin 概率检测法
    a = random.randint(2, n - 2)  # 随机第选取一个a∈[2,n-2]
    s = 0  # s为d中的因子2的幂次数。
    d = n - 1
    while (d & 1) == 0:  # 将d中因子2全部提取出来。
        s += 1
        d >>= 1

    x = quickPower(a, d, n)
    for i in range(s):  # 进行s次二次探测
        x_2 = quickPower(x, 2, n)
        if x_2 == 1 and x != 1 and x != n - 1:
            return False
        x = x_2

    if x != 1:
        return False
    return True


def is_prime(num):
    # 排除0,1和负数
    if num < 2:
        return False

    # 创建小素数的列表,可以大幅加快速度
    # 如果是小素数,那么直接返回true
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                    853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                    991, 997]
    if num in small_primes:
        return True

    # 如果大数是这些小素数的倍数,那么就是合数,返回false
    for prime in small_primes:
        if num % prime == 0:
            return False

    # 如果这样没有分辨出来,就一定是大整数,那么就调用rabin算法
    for i in range(10):
        if not miller_rabin(num):
            return False
    return True


def getLargePrime(size, p=0):
    while True:
        num = random.randrange(2 ** (size - 1), 2 ** size)
        if is_prime(num) and num != p:
            return num


# 找出与（p-1）*(q-1)互质的数e
def co_prime(s):
    while True:
        e = random.randrange(1,s)
        if s < e:
            x = gcd(e, s)
        else:
            x = gcd(s, e)
        if x == 1:  # 如果最大公约数为1，则退出循环返回e
            break
    return e


# 求两个数的最大公约数
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def EX_GCD(a, b, arr):  # 扩展欧几里得
    if b == 0:
        arr[0] = 1
        arr[1] = 0
        return a
    g = EX_GCD(b, a % b, arr)
    t = arr[0]
    arr[0] = arr[1]
    arr[1] = t - (a // b) * arr[1]
    return g


def find_d(a, n):  # ax=1(mod n) 求a模n的乘法逆x
    arr = [0, 1]
    modresult = EX_GCD(a, n, arr)
    if modresult == 1:
        return (arr[0] % n + n) % n
    else:
        exit(-1)


# 生成公钥和私钥
def init_data():
    bit_size = int(input("输入希望的素数位数（bits）："))
    p = getLargePrime(bit_size)
    q = getLargePrime(bit_size, p)

    # print("随机生成两个素数p和q:\np=", p, "\nq=", q)
    n = p * q
    s = (p - 1) * (q - 1)
    e = co_prime(s)
    # print("生成e和d：")
    # print("e=", e)
    d = find_d(e, s)
    # print("d=", d)
    print("生成公钥和私钥：")
    print("公钥: n=", n, "\n\t e=", e)
    print("私钥: n=", n, "\n\t d=", d)
    key = (n, e, d)
    with open(SECRET_KEY_FILE, 'w') as sf:
        sf.write(str(key))
    print("密钥已写入文件(n, e, d):" + SECRET_KEY_FILE)
    return key


# 选择公私钥
def distribute_pk_sk(a, flag):
    pk = (a[0], a[1])  # 公钥
    sk = (a[0], a[2])  # 私钥
    if flag == 0:
        return pk
    if flag == 1:
        return sk


def Calculate(base, exp, mod):  # 快速乘方幂运算
    c = 1
    d = base
    for bit in range(exp.bit_length()):
        if exp & (1 << bit):
            c = c * d % mod
        d = d * d % mod
    return c


# 加密
def rsa(m, pk):
    # 密文B = 明文A的e次方 模 n
    result = Calculate(m, pk[1], pk[0])
    return result


# 解密
def de_rsa(c, sk):
    result = Calculate(c, sk[1], sk[0])
    return result


def encrypt(plain):
    m = plain
    global ps_key
    ps_key = init_data()
    pk = distribute_pk_sk(ps_key, 0)
    m = int(ascll2bit(m, 8), 2)
    c = rsa(m, pk)
    global cipherText
    cipherText = c


def descrypt(cipher):
    c = cipher
    global ps_key
    sk = distribute_pk_sk(ps_key, 1)  # 私钥
    print('签名为:' + str(c))
    m = de_rsa(c, sk)
    out_text = str(bin(m)).replace('0b', '')
    m = ''
    x = len(out_text) % 8
    if x != 0:
        for i in range(8 - x):
            out_text = '0' + out_text
    for i in range(math.ceil(len(out_text) / 8)):
        tmp = out_text[0 + i * 8:8 + i * 8]
        tmp = '0b' + tmp
        tmp = chr(int(tmp, 2))
        m += tmp
    print('解密结果为:')
    print(m)


def sign_verify():
    ReceivedTextFile = open(RECEIVED_TEXT_FILE, 'r')
    receivedtext = ReceivedTextFile.read()
    Digest_re = sha1(receivedtext.encode("utf-8")).hexdigest()
    print("接受到的消息进行摘要：")
    print(Digest_re)
    pass

if __name__ == "__main__":
    #plainText = input("请输入明文:")
    PlainTextFile = open(PLAIN_TEXT_FILE, 'r')
    plainText = PlainTextFile.read()
    Digest = sha1(plainText.encode("utf-8")).hexdigest()
    PlainTextFile.close()
    print("明文摘要为：")
    print(Digest)
    encrypt(Digest)
    descrypt(cipherText)
    sign_verify()