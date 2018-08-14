lines=open('hashes.txt').readlines()
hashes=[l.split(',')[1] for l in lines]
assert all(len(h)==64 for h in hashes)
print('count:',len(hashes))
hashes=[int(h,16) for h in hashes]

def diff(h1,h2):
    d=0
    x=h1^h2
    for i in range(256):
        if (x>>i)&1==0:
            d+=1
    return d

maxdiff=0
for i,h in enumerate(hashes):
    print(i,'/',len(hashes))
    for j,h2 in enumerate(hashes):
        if j>=i:
            break
        if diff(h,h2)>maxdiff:
            maxdiff=diff(h,h2)
            print(maxdiff,i,j)

print(maxdiff,i,j)
