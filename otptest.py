#Copyright 2017 Drew Griess (DOCTOREWW)
#THIS WAS CREATED BY DOCTOREWW
#PLEASE GIVE IT CREDIT WHERE CREDIT IS DUE

#Rhyme intended
from binascii import hexlify,unhexlify
from getpass import getpass
from sys import stdin
import hashlib,string,random,onetimepad
def hashsha(hashin):
    return (hashlib.sha512(hashin.encode()).hexdigest())

###########NOTES###########
#hash(hash(salt+Password1*x)+hash(salt+password2*x)) where x is number of itterations x>2
#should i make the hashes for each stage diffrent so if one hashing algerithm is secritly comprimised it is still parshly secure?
#Should I implement key streching and make it take longer to guess?
#can you break this from non brute force provided the file keeps its integrity ?
#Is this implimentation of the imported OTP valid

def makesalt():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
def LRH(password1,password2,length,saltpre):
    #THIS LOOKS UGLY HOW SHOULD I MAKE BETTER
    seed=""#add a shared secrit here to decrease the chance of bruting the password
    salt=hashsha(saltpre+seed)
    i=2
    resulthash=""
    while(len(resulthash)<length):
        hashthing=hashsha(hashsha(salt*i+password1*i)+hashsha(salt*i+password2*i)+salt)
        resulthash+=hashthing
        i+=1
    return resulthash[0:length]
def encryptme(password1,password2,message,salt):
    x=hexlify(message).decode("utf8")
    return onetimepad.encrypt(x, LRH(password1,password2,len(x),salt))
def decryptme(password1,password2,message,salt):
    return unhexlify(onetimepad.decrypt(message, LRH(password1,password2,len(message),salt)))
def getFile(files):
    import binascii
    with open(files, 'rb') as f:
        return (binascii.hexlify(f.read()))
def encryptfile(salt):
    print("Please help me troubleshoot this encryption method on github")
    inputfile=input("What file would you like to encrypt?\n")
    message=getFile(inputfile)
    text_file = open(inputfile+".encrypted", "w")
    text_file.write(salt+encryptme(getpass("What is password ONE:\n"),getpass("What is password TWO:\n"),message,salt))
    text_file.close()
def decryptfile():
    text_file=open(input("What file would you like to decrypt?\n"),"r")
    encryptedtext=text_file.read()
    text_file.close()
    salt=encryptedtext[0:15]
    originalfile=unhexlify(decryptme(getpass("What is password ONE:\n"),getpass("What is password TWO:\n"),encryptedtext[15:],salt))
    output=input("What would you like to name this unencrypted file?\n")
    with open(output, 'wb') as f:
        f.write(originalfile)
encryptfile(makesalt())
decryptfile()


#Copyright 2017 Drew Griess (DOCTOREWW)
#drewgriess.com
