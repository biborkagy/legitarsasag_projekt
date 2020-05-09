text=""
f=open("after_z.txt","r")
for sor in f:
    text+=sor.strip()
    

f.close()
#print(text)
db=0
atlag=0
szamok=['0','1','2','3','4','5','6','7','8','9']
elozo_karakter=text[0] #ez lesz mindig az, ami, ha 'z', akkor utána megvizsgáljuk, hogy szám van_e
for i in range( len(text)-1): #utolsó előtti karakterig megyünk
    
    if elozo_karakter=='Z' and (text[i] in szamok):
        print(elozo_karakter,' ', text[i])
        db+=1
        atlag+=int(text[i])
    elozo_karakter=text[i] #átírjuk az ekozo karaktert
    
print(atlag)
print(atlag/db)
print("keresett szám:",round(atlag/db,0))
