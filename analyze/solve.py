import requests
import base64
import hashlib
import datetime
import subprocess
import string

host = "http://127.0.0.1:5000/"

session = requests.Session()

def getjob():
    r = session.post(host+'getjob').json()
    return r['suffix'].encode()

def submitjob(nonce1, nonce2, coin):
    payload={
        'nonce1': base64.b64encode(nonce1),
        'nonce2': base64.b64encode(nonce2),
        'coin': coin
    }
    r = session.post(host+'submitjob', data=payload).json()
    return r

print('Running tests')
print(submitjob(b'a',b'a',0))
suffix=getjob()
print(submitjob(b'a',b'a',b'a'))
print(submitjob(b'a',b'a',0))
print(submitjob(b'a',b'b',3))
print(submitjob(b'a',b'b',0))

print('Trying md5 collision')
msg1=bytes.fromhex('4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2')
msg2=bytes.fromhex('4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2')
assert msg1!=msg2 and hashlib.md5(msg1).hexdigest()==hashlib.md5(msg2).hexdigest()
assert hashlib.md5(msg1+suffix).hexdigest()==hashlib.md5(msg2+suffix).hexdigest()
print(submitjob(msg1,msg2,0))

print('Trying sha1 collision')
suffix=getjob()
msg1=open('shattered-1.pdf','rb').read()
msg2=open('shattered-2.pdf','rb').read()
print(submitjob(msg1,msg2,1))

print('Solving sha256')
hashes=[l.split(',')[1] for l in open("hashes.txt").readlines()]
indices=[[int(s) for s in l.split()] for l in open("diff199_result.txt").readlines()]
hashdata=[eval(s) for s in open("hashdata.txt").readlines()]
dic={k:v for _,k,v in hashdata}
sols={}
for _,i1,i2 in indices:
    if dic[hashes[i1]][-1]==dic[hashes[i2]][-1]:
        if chr(dic[hashes[i1]][-1]) in string.ascii_letters + string.digits:
            sols[dic[hashes[i1]][-1]]=(dic[hashes[i1]][:-1],dic[hashes[i2]][:-1])
print(sols.keys())
while True:
    suffix=getjob()
    print(suffix[0:1])
    if suffix[0] in sols:
        print(submitjob(*sols[suffix[0]],2))
        break

print('Bruteforce md5')
suffix=getjob()
print(datetime.datetime.now())
with open('md5.bin','wb') as f:
    for i in range(2*1024*1024):
        f.write(hashlib.md5(str(i).encode()+suffix).digest())
print('Running c code')
result = subprocess.check_output(['./bruteforcediff'])
print(result)
i1,i2,_=[int(s) for s in result.split()]
print(submitjob(str(i1).encode(),str(i2).encode(),0))
