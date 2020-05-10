#Számoljuk össze (egy megírt program segítségével) hányszor szerepel a szövegben az X, Y és W karakter. Az eredmény: X_száma + Y_száma - W_száma

with open( 'count-x-y-w.txt' ) as f:
    t = f.read()

res = int( t.count('X')) + int( t.count('Y')) - int( t.count('W') )
print( 'eredmény:', res )

with open( 'result_count_xyw.txt', 'w' ) as f:
    print( f'X db + Y db - W db =  {res}', file = f )
