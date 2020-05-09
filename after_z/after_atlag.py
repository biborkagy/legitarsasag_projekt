text=""
f=open("after_z.txt","r")
text=f.read()
f.close()
#print(text)
db=0
atlag=0
szamok=['0','1','2','3','4','5','6','7','8','9']
for karakter in text:
    if karakter in szamok:
        db+=1
        atlag+=int(karakter)
#print(atlag)
#print(atlag/db)
print("keresett szám:",round(atlag/db,0))
