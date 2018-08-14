import requests
import traceback
import hashlib
import datetime

hashes=[l.split(',')[1] for l in open("hashes.txt").readlines()]
index=[l.split()[1:] for l in open("diff199_result.txt").readlines()]
index=set(int(i) for i,j in index)|set(int(j) for i,j in index)
index=sorted(list(index))
print(len(index))

def gethashdata(blockhash):
    j = requests.get("https://blockchain.info/rawblock/"+blockhash).json()
    ver=j['ver']
    prev=j['prev_block']
    mrkl=j['mrkl_root']
    t=j['time']
    bits=j['bits']
    nonce=j['nonce']

    def rev(x):
        return ''.join([x[i-2:i] for i in range(len(x),0,-2)])

    def tohex(x):
        return rev(format(x,'08x'))

    d=tohex(ver)+rev(prev)+rev(mrkl)+tohex(t)+tohex(bits)+tohex(nonce)
    d=bytes.fromhex(d)
    assert rev(hashlib.sha256(hashlib.sha256(d).digest()).hexdigest())==blockhash
    return hashlib.sha256(d).digest()

with open('hashdata.txt') as f:
    hashdata=[eval(s) for s in f.readlines()]
dic={k:v for _,k,v in hashdata}

with open('hashdata.txt','a') as f:
    for k,i in enumerate(index):
        h=hashes[i]
        if h in dic:
            continue
        d=None
        try:
            d=gethashdata(h)
        except Exception as e:
            traceback.print_exc()
        print(repr((i,h,d)),file=f)
        f.flush()
        print(datetime.datetime.now(),k,'/',len(index),repr((i,h,d)))

