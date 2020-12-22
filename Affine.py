# 穷举密钥破解
import sys

la = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
lb = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
      14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]


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


# 加密
def encrypt(m, c, a, b):
    for i in range(len(m)):
        if m[i] != ' ':
            # 加密成相应的大写字母
            c.append(chr(((ord(m[i]) - 97) * a + b) % 26 + 65))
        else:
            c.append(' ')
    d = ''.join(c)
    print(d)


# 解密
def decrypt(c, k, b):
    mw = []
    for i in range(len(c)):
        if c[i] != ' ':
            tmp = ord(c[i]) - 65 - b
            if tmp < 0:
                tmp += 26
            mw.append(chr((k * tmp) % 26 + 97))
        else:
            mw.append(' ')
    print("k=" + str(k) + ", b=" + str(b) +"时，解密后的明文为：")
    res = ''.join(mw)
    print(res)


# 实现

    #密文
if __name__ == "__main__":
        #
        # 明文
    # m = (input("请输入明文：")).lower()
    # c = []
    # x = input("请输入密钥a(与26互素): ")
    # y = input("请输入密钥b(小于26): ")
    # a = int(x)
    # b = int(y)
    # while gcd(a, 26) != 1:
    #     x, y = input("a和26不互素，请重新输入a和b: ").split()
    #     a = int(x)
    #     b = int(y)
    # print("明文内容为：")
    # print(m)
    # print("加密后的密文为：")
    # encrypt(m, c, a, b)
    # print("已知密钥破解：")
    k = Modreverse(13, 2436)
    print(k)
    # decrypt(c, k, b)
    # print("穷举密钥破解如下： ")
    # for i in range(0, 12):
    #     for j in range(0, 26):
    #         decrypt(c, la[i], lb[j])
