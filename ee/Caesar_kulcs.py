# Caesar kulcs

#1. 
'''
Fibonacci 50
Az ötvenedik fibonacci szám legmagasabb helyiértékű számjegye kivonva a legkisebb helyiértéküből. Ha a nulladik: 0, az első: 1.
'''
lista =  [0,1]
n = 49
for i in range(n):
    lista.append( lista[i] + lista[i+1])
s = str(lista[49])
res1 = int( s[-1] ) - int( s[0] )
print(res1)

# 2.
'''
after_z.txt
Keressük ki a file-ban a Z karakter után következő számjegy karatereket és az átlaguknak vegyük az egész részét.
'''
with open('after_z.txt') as f:
    txt = f.read()

n = len(txt)
lista = []
for i in range(n-1):
    if txt[i] == 'Z':
        for j in range(i+1,n):
            if txt[j].isnumeric() :
                lista.append( int(txt[j]) )
            else:
                break
res2 = int( sum(lista) / len(lista) ) 
print( res2 )

# 3.Számoljuk össze hányszor szerepel a szövegben az X, Y és W karakter.
# Az eredmény: X_száma + Y_száma - W_száma

with open( 'count-x-y-w.txt' ) as f:
    t = f.read()

res3 = int( t.count('X')) + int( t.count('Y')) - int( t.count('W') )
print( res3 )

Caesar_kulcs = res1 + res2 + res3

with open( 'Caesar_kulcs.txt', 'w' ) as f:
    print('Caesar_kulcs.txt', Caesar_kulcs )
    print('Caesar_kulcs.txt', Caesar_kulcs, file = f )
