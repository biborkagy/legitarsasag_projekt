def titkosít(txt, k):
    a, z, A, Z = ord('a'), ord('z'), ord('A'), ord('Z')
    n = z - a + 1
    res = ''
    for c in txt:
        if c.isalpha():
            if  c.isupper():
                res += chr((ord(c) + k - A) % n + A)
            else:
                res += chr((ord(c) + k - a ) % n + a)
        else:
            res+= c
    return res
    
with open('caesar.txt') as f:
    lista = f.readlines()

txt = ''
for sor in lista:
    txt += titkosít(sor,-16)
        
with open('caesar_decoded.txt','w') as f:
    print(txt, file=f)
    print(txt)
