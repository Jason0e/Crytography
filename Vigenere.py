
#加密
def encrypt(m,c,k,k0):
    for i in range(len(m)):
        if m[i] != ' ':
            # 加密成相应的大写字母
            c.append(chr(((ord(m[i]) - 97)  + (ord(k[i])-97)%len(k0)) % 26 + 65))
        else:
            c.append(' ')
    d = ''.join(c)
    print(d)
    return

#解密
def decrypt(c,kt,kt0):
    m = []
    for i in range(len(c)):
        if c[i] != ' ':
            m.append(chr(((ord(c[i]) - 65)  - (ord(kt[i])-65)%len(kt0)) % 26 + 97))
        else:
            m.append(' ')
    d = ''.join(m)
    print(d)
    return

if __name__ == "__main__":
    #
    # 明文
    m = (input("请输入明文：")).lower()
    lm = len(m) #明文长度
    # 密钥
    k0 = (input("请输入密钥：")).lower()#原始密钥
    k = k0*(lm//len(k0))
    ki=list(k)
    for i in range(lm):
        if m[i] == ' ':
            ki.insert(i,' ')
    k = ''.join(ki)#扩充密钥
    print(k)
    #密文
    c=[]
    print("明文内容为：")
    print(m)
    print("加密后的密文为：")
    encrypt(m, c, k, k0)
    print("解密\n")
    kt0 = (input("请输入密钥：")).lower() #原始密钥
    kt = kt0*(lm//len(kt0))
    kti=list(kt)
    for i in range(lm):
        if m[i] == ' ':
            kti.insert(i,' ')
    kt = ''.join(ki)#扩充密钥
    print("解密后明文为：")
    #print(c)
    decrypt(c,kt,kt0)