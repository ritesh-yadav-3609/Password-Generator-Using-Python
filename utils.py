import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import os
import json

"""  This function swap the array Randomly  """
def swaper(f1,f2,full,inc,seperator1,seperator2):
    n = len(full)
    for i in range(f1,f2,inc):
        r1 =i*seperator1+seperator2
        r2 =i*seperator2+seperator1
        r1, r2 = r1%n, r2%n
        temp = full[r1]
        full[r1] = full[r2]
        full[r2] = temp
    return full

"""  This function is used convert Binary to Decimal """
def binaryToDecimal(num):
    b_num = list(num)
    value = 0
    for i in range(len(b_num)):
        digit = b_num.pop()
        if digit == '1':
            value = value + pow(2, i)
    return value

"""  This function remove character from string Randomly """
def remover(password, num, indexs, n):
    temp = list(password)
    i = num
    while len(indexs)>n:
        for x in indexs:
            i +=x
            i *=len(str(num))
        i = i%len(indexs)
        temp.pop(indexs.pop(i))
        indexs = indexs[0:i]+[ (n-1) for n in indexs[i:]]
    return ''.join(map(str, temp))

"""  This remove unwanted upper case Character """
def removeUper(password, num, upper_num):
    indexs = []
    for i,p in enumerate(password):
        if p.isupper():
            indexs.append(i)
    return remover(password,num, indexs, upper_num)

"""  This remove unwanted lower case Character """
def removeLower(password, num, lower_num):
    indexs = []
    for i,p in enumerate(password):
        if p.islower():
            indexs.append(i)
    return remover(password,num, indexs, lower_num)

"""  This remove unwanted digit """
def removeNum(password, num, number_num):
    indexs = []
    for i,p in enumerate(password):
        if p.isnumeric():
            indexs.append(i)
    return remover(password,num, indexs, number_num)

"""  This remove unwanted symbol """
def removeSymbol(password, num, symbol_num):
    indexs = []
    for i,p in enumerate(password):
        if not (p.isalpha() or p.isnumeric()):
            indexs.append(i)
    return remover(password,num, indexs, symbol_num)

"""  This create public and private key's """
def rsakeys():  
    length=1024  
    privatekey = RSA.generate(length, Random.new().read)  
    publickey = privatekey.publickey()  
    return privatekey, publickey

"""  This encrypt the string using public key """
def encrypt(rsa_publickey,plain_text):
    cipher_text=rsa_publickey.encrypt(plain_text,128)[0]
    b64cipher=base64.b64encode(cipher_text)
    return b64cipher

"""  This decrypt the string using private key """ 
def decrypt(rsa_privatekey,b64cipher):
    decoded_ciphertext = base64.b64decode(b64cipher)
    plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
    return plaintext

"""  This function read the data from file for retriving password """
def readfile(file_data, seperator1,seperator2):
    full = file_data.split(",")
    n = len(full)
    full = swaper(n-1,-1,full,-1,seperator1,seperator2)
    values = ''.join(chr(binaryToDecimal(x)) for x in full)
    l1, l2 = int(values[0]), int(values[-1])
    values = values[1:-1]
    n = len(values)-l1-l2
    r2 = values[seperator2%n:seperator2%n+l2]
    values = values.replace(r2,"")
    r1 = values[seperator1%n:seperator1%n+l1]
    values = values.replace(r1,"")
    r1, r2=int(r1), int(r2)
    private_string = values[0:r1]
    values = values[r1:]
    public_string = values[-r2:]
    values = values[:-r2]
    privatekey = RSA.importKey(private_string)
    publickey = RSA.importKey(public_string)
    dic = {}
    while len(values)>0:
        i = values[0]
        l = values[1:int(i)+1]
        res = values[int(i)+1:int(l)+int(i)+1]
        values = values[int(l)+int(i)+1:]
        res = json.loads(decrypt(privatekey,res).decode("utf-8"))
        if "sn" in res and "un" in res and "ln" in res and "dn" in res:
            dic["snunlndntistpsts"]=res
        else: 
            dic[res["username"]+res["web"]+res["type"]]=res
    return privatekey, publickey, dic

"""  This function read the random number from file for retriving password """
def getTime(data,filename,generate,values1,values2,sd):
    if not os.path.exists(filename):
        f= open(filename,"w+")
    with open(filename) as f:
        file_data = f.read()
    if len(file_data)>0:
        _, __, time_data = readfile(file_data, values1,values2)
        key = data["username"]+data["web"]+data["type"]
        if key in time_data and not generate:
            data["time"]=time_data[key]["time"]
        if "snunlndntistpsts" in time_data:
            sd = time_data["snunlndntistpsts"]
    return data, sd

