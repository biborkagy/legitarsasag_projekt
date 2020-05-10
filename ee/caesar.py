def caesar_dekodoló(ch, k):
    c = ord( ch )
    a = ord('a')
    z = ord('z')
    A = ord('A')
    Z = ord('Z')
    if ch.isalpha():
        if (a <= c <= z):
            if a <= c-k:
                return chr(c-k)
            else:
                return chr( z - a - k + c +1)
        if A <= c <= Z:
            if A <= c-k:
                return chr(c-k)
            else:
                return chr( Z - A - k + c +1)
    else:
        return ch 

with open('caesar.txt') as f:
    lista = f.readlines()

txt = ''
for sor in lista:
    for c in sor:
        txt += caesar_dekodoló(c,16)
    #txt += '\n'
        
print(txt)
with open('caesar_decoded.txt','w') as f:
    print(txt, file=f)
