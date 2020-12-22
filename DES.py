import random
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码


#########文件变量
CIPHER_TEXT_FILE = "cipherText.txt"   #密文文件
PLAIN_TEXT_FILE = "plainText.txt"     #明文文件
SECRET_KEY_FILE = "secretKey.txt"     #密钥文件
DECRYPT_TEXT_FILE = "decryptText.txt" #解密文件


IP_Table = [  # IP置换矩阵
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
E_Table = [  # 扩展矩阵E盒
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
P_Table = [  # P 盒
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
IPR_Table = [  # 逆IP置换矩阵
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
PC1_Table = [  # 密钥第一次置换矩阵
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
PC2_Table = [  # 密钥第二次置换矩阵
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
S_Box = [  # 8个S盒
    # S1
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13, ],
    # S2
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9, ],
    # S3
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12, ],
    # S4
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14, ],
    # S5
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3, ],
    # S6
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13, ],
    # S7
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12, ],
    # S8
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

######int转二进制

def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

#######异或操作
def XOR(s1,s2):
    length = len(s1)
    xorResult = []
    for i in range(0, length):
        # 转为int类型0，1比特，进行异或操作后，转为string类型
        xorResult.extend(str(int(s1[i]) ^ int(s2[i])))
    return xorResult

######表格置换函数
"""
    function: transfrom the binaryStr with the giver permutation table
    condition: len(binaryStr) == len(PermutationTable)
    return: the permutated binary List.
"""

def Permutation(binaryStr, PermutationTable):
    length = len(PermutationTable)
    PermutatedList = []
    for i in range(0, length):
        PermutatedList.extend(binaryStr[PermutationTable[i] - 1])
    return PermutatedList

#####循环左移指定位数

def shiftLeft(binaryStr, nBits):
    length = len(binaryStr)
    nBits = nBits % nBits
    shiftedList = list(binaryStr)
    for i in range(0, length):
        if i < nBits:
            shiftedList.extend(shiftedList[0])
            del shiftedList[0]
        else:
            break
    return shiftedList
#########################

#######字节转比特
def ByteToBit(ByteString):
    bitList = []
    for i in range(0,4):
        bitList.insert(0, str(ByteString%2))
        ByteString = int(ByteString / 2)
    bitResult = "".join(bitList)
    return bitResult

######生成密钥

######PC_1置换

def PC_1_Permutation(SecretKey):
    PC_1_Result = Permutation(SecretKey, PC1_Table)
    C_0 = PC_1_Result[0: int(len(PC_1_Result)/2)]
    D_0 = PC_1_Result[int(len(PC_1_Result)/2): int(len(PC_1_Result))]
    return C_0, D_0

#####循环左移函数
def RingShiftLeft(str_28_bits, ShiftFlag):
    LshiftResult = ""
    if ShiftFlag == 1 or ShiftFlag == 2 or ShiftFlag == 9 or ShiftFlag == 16:
        LshiftResult = shiftLeft(str_28_bits, 2)
    else:
        LshiftResult = shiftLeft(str_28_bits, 1)
    return LshiftResult

#####PC_2置换
def PC_2_Permutation(str_56_bits):

    #  去掉9， 18， 22， 25， 35， 38，43， 54 位
    str_48_bits = Permutation(str_56_bits, PC2_Table)
    return str_48_bits


####创建子密钥
"""
    function: create the 16 son keys with the given key
    return: sonKeysList: 16 son keys list
"""
def createSonKey(SecretKey):
    # 提取密钥中的非校验位
    str_56_bits_List = list(SecretKey)
    sonKeyList = []
    # 获取子密钥
    Temp_PC_1_PermutationResult_C_i_1, Temp_PC_1_PermutationResult_D_i_1 = PC_1_Permutation(str_56_bits_List)
    C_i = []
    D_i = []
    for i in range(1, 17):
        # C_i-1 D_i-1
        # 计算C_i D_i
        if i == 1 or i == 2 or i == 9 or i == 16:
            C_i = shiftLeft(Temp_PC_1_PermutationResult_C_i_1, 1)
            D_i = shiftLeft(Temp_PC_1_PermutationResult_D_i_1, 1)
        else:
            C_i = shiftLeft(Temp_PC_1_PermutationResult_C_i_1, 2)
            D_i = shiftLeft(Temp_PC_1_PermutationResult_D_i_1, 2)
        CD = C_i + D_i
        sonKey_i = PC_2_Permutation(CD)
        sonKeyList.append(sonKey_i)
        Temp_PC_1_PermutationResult_C_i_1 = C_i
        Temp_PC_1_PermutationResult_D_i_1 = D_i
        if i == 16:
            break
    return sonKeyList


######IP置换
def InitialPermutation(M_0):

    IP_Result = Permutation(M_0, IP_Table)
    L_0 = IP_Result[0:int((len(IP_Result)/2))]
    R_0 = IP_Result[int((len(IP_Result)/2)):int(len(IP_Result))]
    return L_0, R_0  # List type

#####E盒扩展置换
def E_Expand(R_i_1):

    E_R_i_1 = Permutation(R_i_1, E_Table)
    return E_R_i_1

######S盒代换
def S_Box_Transformation(six_bits_str, S_Box_Num):

    row = int(six_bits_str[0]) * 2 + int(six_bits_str[5])
    col = int(six_bits_str[1]) * 8 + int(six_bits_str[2]) * 4 + int(six_bits_str[3]) * 2 + int(six_bits_str[4])
    value = S_Box[int(S_Box_Num - 1)][int(row * 15 + col)]
    four_bits_str = list(int2bin(value,4))
    return four_bits_str
#####P盒置换
def P_Permutation(str_32bits):

    FeistelResult = Permutation(str_32bits, P_Table)
    return FeistelResult

#####轮函数
def Feistel(R_i_1, K_i):

    E_ExpandResult = E_Expand(R_i_1)
    xorResult = XOR(E_ExpandResult, K_i)
    str_32_bits = []
    for i in range(8):
        str_6_bits = xorResult[i * 6: i * 6 + 6]
        str_32_bits += S_Box_Transformation(str_6_bits, i + 1)
    return "".join(P_Permutation(str_32_bits))


######P逆置换
def InversePermutation(R_16_L_16):

    cipherText = ""
    cipherText = Permutation(R_16_L_16, IPR_Table)
    return cipherText

######加密交叉迭代过程
def CrossIterationInEncryption(L_0, R_0, SecretKey):

    R = ""
    L = ""
    tmp_R = R_0
    tmp_L = L_0
    sonKeyList = createSonKey(SecretKey)
    for i in range(1,17):
        L = tmp_R
        R = XOR(tmp_L,Feistel(tmp_R,sonKeyList[i - 1]))
        tmp_R = R
        tmp_L = L
        LM = "".join(L)
        RM = "".join(R)
        print('L%d'% i,hex(int(LM,2)),"\t")
        print('R%d'% i,hex(int(RM,2)))
        # print('L%d' % i, LM, "\t")
        # print('R%d' % i, RM,)
    RL = R + L
    return RL

######解密交叉迭代过程
def CrossIterationInDecryption(L_0, R_0, SecretKey):

    R = []
    L = []
    tmp_R = R_0
    tmp_L = L_0
    sonKeyList = createSonKey(SecretKey)
    for i in range(1,17):
        L = tmp_R
        R = XOR(tmp_L,Feistel(tmp_R,sonKeyList[16 - i]))
        tmp_R = R
        tmp_L = L
    LM = "".join(L)
    RM = "".join(R)
    print("L%d              R%d" % (i,i))
    print("%h\t%h" % (hex(int(LM,2)),hex(int(RM,2))))
    RL = R + L
    return RL
######加密函数
def Encryption(plainText, secretKey):

    print("加密过程：\n")

    M = list(plainText)
    L0, R0 = InitialPermutation(M)
    RL = CrossIterationInEncryption(L0, R0, secretKey)
    cipherText = "".join(InversePermutation(RL))
    return cipherText


######随机生成KEY
def createSecretKey():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    key = []
    for i in range(8):
        key.append(random.choice(seed))
    randomSecretKey = ''.join(key)
    return randomSecretKey
######8个字符的字符串转为ascii，然后转 0 1串
def ToBitString(string_8_char):
    strList = []
    for i in range(8):
        strList.append(str(int2bin(ord(string_8_char[i]), 8)))
    return "".join(strList)
########64位bits转为8个ascii字符
def ToAsciiChar(string_64_bits):
    strList = []
    bitList = list(string_64_bits)
    for i in range(8):
        if int("".join(bitList[i * 8: i * 8 + 8]), 2) < 8:
            continue
        # 八个bit一个处理单元，先转为10进制，然后转ascii，存入列表
        strList.append(chr(int("".join(bitList[i * 8: i * 8 + 8]), 2)))
    #print("ASCII:" + str(strList))
    return "".join(strList)


if __name__ == "__main__":

    #secretKey = createSecretKey()
    #随机生成密钥

    # flag = input("请输入：0)退出; 1）加密; 2）解密：")

    secretKey = input("请输入密钥（8位）：")
    with open(SECRET_KEY_FILE, 'w') as sf:
        sf.write(secretKey)
    print("密钥已写入文件" + SECRET_KEY_FILE + "!")
    secretKeyBitString = ToBitString(secretKey)
    # print("得到密钥的 0 1字符串！")

    full_flag = True  # 分组为8的倍数的标志，为8则真
    PlainTextFile = open(PLAIN_TEXT_FILE, 'r')
    CipherTextFile = open(CIPHER_TEXT_FILE, 'w',encoding='utf-8')
    DecryptTextFile = open(DECRYPT_TEXT_FILE, 'w',encoding='utf-8')
    while True:
        text_8_bytes = PlainTextFile.read(8)
        if len(text_8_bytes) != 8:
            full_flag = False
        if not text_8_bytes:
            print("读取明文文件结束")
            break


        # else:
        #     bitString = ToBitString(text_8_bytes)
        #     # 加密
        #     encryptStr = Encryption(bitString, secretKeyBitString)
        #     # 加密结果写入文件
        #     CipherTextFile.write(str(ToAsciiChar(encryptStr)))

        if full_flag == True:#不需要填充
            NumOfLostBytes = 8 - len(text_8_bytes)
            bitStringList = []
            for i in range(len(text_8_bytes)):
                bitStringList.append(int2bin(ord(text_8_bytes[i]), 8))

            full_8_bits = int2bin(NumOfLostBytes, 8)  # 填充的比特串
            # 填充的字节数 转为bitstring
            for i in range(NumOfLostBytes):
                bitStringList.append(full_8_bits)
            bitString = "".join(bitStringList)  # 补全64位分组
            # 加密
            encryptStr = Encryption(bitString, secretKeyBitString)
            # 加密结果写入文件
            CipherTextFile.write(str(ToAsciiChar(encryptStr)))

        # 读取完整的8个字节分组字节，尾部填充8个字节，取值都为08
        if full_flag == False:
            zero_eight = "00001000"
            tmpList = []
            for i in range(8):
                tmpList.append(zero_eight)
            bitString = "".join(tmpList)
            # 加密
            encryptStr = Encryption(bitString, secretKeyBitString)
            # 加密结果写入文件
            CipherTextFile.write(str(ToAsciiChar(encryptStr)))

    PlainTextFile.close()
    CipherTextFile.close()
    with open(PLAIN_TEXT_FILE, 'r') as pf:
        data = pf.read()
        print("明文为：")
        print(data)
    # with open(CIPHER_TEXT_FILE, 'r') as cf:
    #     data = cf.read()
    print("加密结果为：")
    print(hex(int(encryptStr,2)))
