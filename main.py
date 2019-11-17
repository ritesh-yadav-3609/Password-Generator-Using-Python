import json
import os
import random
from datetime import datetime
from Crypto.PublicKey import RSA
from utils import swaper, binaryToDecimal, removeLower, removeUper, removeNum, removeSymbol, rsakeys, encrypt, decrypt, getTime, readfile

"""  This function generate 20 digit random value for time variable """
def make20(op, sd, num = "123456789"):
    string20 = num
    now = datetime.now()
    t = [str(now.year)+str(now.month)+str(now.day),str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond),str(int(datetime.timestamp(now)))]
    for i,o in enumerate(op):
        st = str(abs(int(eval(t[i%3]+o+t[2-(i%3)]+o+str(int(string20))))))
        string20 = string20+st
        if len(string20)>sd["ts"]:
            string20 = string20[-sd["ts"]:len(string20)]
    return string20

"""  This function generate random password for using all variables """
def generator(data,count, sd):
    password_index = ""
    password = ""
    st = data["username"]+data["time"]+str(count)+data["web"]+data["type"]
    binary = ''.join(format(ord(x), 'b') for x in st)
    n = len(st)
    l = []
    with open('data/data.df') as f:
        data = f.read()
        digit_size = len(data)
        l = [binaryToDecimal(binary[i:i+n])%digit_size for i in range(0, len(binary), n)]
        start_point = 1
        for x in l:
            start_point += x
            start_point *= x
            start_point /= n
            start_point = int(start_point)
        n1 = len(str(digit_size))+1
        start_point = (start_point%(digit_size))-n1
        for i in range(0,sd["tis"]):
            password_index += data[start_point:start_point+n1]
            start_point = (int(int(data[start_point:start_point+n1])*l[i%len(l)]/n1+l[i%len(l)])%(digit_size))
    
    with open('data/data.cf') as f:
        data = f.read()
        char_size = len(data)
        n1 = len(str(char_size))+1
        start_point = n*int(password_index[1:10])%char_size
        for i in range(0,sd["tps"]):
            password += data[start_point]
            index = int(password_index[(i*start_point%n1)%len(password_index)-1])
            start_point = (int(index*l[i%len(l)]/n1+l[i%len(l)])%(char_size+n1))-1
    if len(password_index)>0:
        password = removeSymbol(password, l[-4], sd["sn"])
        password = removeUper(password,l[-1], sd["un"])
        password = removeNum(password, l[-2], sd["dn"])
        password = removeLower(password, l[-3], sd["ln"])
        
    return password

"""  This function is used to save all info required for retrieving password in given file """
def save(data,filename, seperator1,seperator2, sd):
    publickey = ""
    privatekey = ""
    values = {}
    if not os.path.exists(filename):
        f= open(filename,"w+")
    with open(filename) as f:
        file_data = f.read()
    if len(file_data)>0:
         privatekey, publickey, values = readfile(file_data, seperator1, seperator2)
    else:
        privatekey,publickey=rsakeys()
    values[sv] = sd
    values[data["username"]+data["web"]+data["type"]]=data
    result = ""
    for i in values:
        res = json.dumps(values[i])
        res=encrypt(publickey,res.encode()).decode("utf-8")
        result += str(len(str(len(res))))+str(len(res))
        result += res
    private_string = privatekey.exportKey("PEM").decode("utf-8")
    public_string = publickey.exportKey("PEM").decode("utf-8")
    full_string = private_string+result+public_string
    full_string = list(full_string)
    r1 = len(private_string)
    r2 = len(public_string)
    n = len(full_string)
    full_string.insert(seperator1%n,r1)
    full_string.insert(seperator2%n,r2)
    full_string.insert(0,len(str(r1)))
    full_string.insert(len(full_string),len(str(r2)))
    full_string = ''.join(map(str, full_string))
    full = ','.join(format(ord(x), 'b') for x in full_string).split(",")
    n = len(full)
    file1 = open(filename, "w")
    full = swaper(0,n,full,1,seperator1,seperator2)
    file1.write(','.join(map(str, full)))

def main(sd):
    assert len(values)==3, "Enter three number seperated by single space(' ')"
    assert (values[0].isnumeric() and values[1].isnumeric() and values[2].isnumeric()), "Enter only number"
    data = user_data
    assert len(data)>=4 and "time" in data and "type" in data and "web" in data and "username" in data, "All data is not present in user_data variable"
    data, sd = getTime(data,filename,generate,int(values[1]),int(values[2]), sd)
    counter = 0
    for p in data["time"]:
        if (p.isalpha() or p.isnumeric()):
            counter=1
    if generate and counter==0:
        data["time"] = make20(data["time"],sd,values[1])
        print(generator(data,values[0],sd))
        save(data, filename,int(values[1]),int(values[2]), sd)
    elif len(data["time"])>=20:
        print(data)
        print(generator(data,values[0],sd))
    else:
        print("Envalid input")

if __name__ == "__main__":
    sv = "snunlndntistpsts"
    sd = {
        "sn" :      4,      # Value for number of symbol present in password
        "un" :      3,      # Value for number of upper case character present in password
        "ln" :      4,      # Value for number of lower case character present in password
        "dn" :      2,      # Value for number of digit present in password
        "tis" :     20,     # Value for size of temp digit
        "tps" :     50,     # Value for size of temp password
        "ts" :      20      # Value for size of random number
    }
    """ Values for user password change """
    generate = False                        # Boolean value for password generated or retriving
    filename = "../data.txt"                # Enter file name for storing Credentials
    user_data = { 
                "web"       : "testweb",    # Enter website or application name
                "username"  : "tester",     # Enter username or email id
                "type"      : "pass",        # Type shoud be pin or password
                "time"      : "+-/*+-"   # Enter at least 5 operational symbol ( from -,+,%,*,/)
            }
    values = "1234567 12345 12345".split(" ")      # Enter 3 number any range seperated by single space (i.e. ' ')
    main(sd)        
