import requests
import datetime
max_height=536557
max_time=1534118400000

def gethash(height):
    j=requests.get('https://blockchain.info/block-height/'+str(height)+'?format=json').json()
    if len(j['blocks'])!=1:
        print('too many blocks at '+str(height))
    else:
        return j['blocks'][0]['hash']

def getblocksofday(time):
    j=requests.get('https://blockchain.info/blocks/'+str(time)+'?format=json').json()
    return sorted([(b['height'], b['hash'], b['time'], b['main_chain']) for b in j['blocks']],
            key=lambda x:-int(x[0]))

with open('hashes.txt','a') as f:
    for time in range(max_time, 0, -1000*3600*24):
        if time>1496880250000-1000*3600*24:
            continue
        blocks=getblocksofday(time)
        for b in blocks:
            print(b[0],b[1],datetime.datetime.fromtimestamp(int(b[2])),b[3], sep=',')
            print(*b, sep=',', file=f)
