from googlesearch import search
import sqlite3
import pprint

conn = sqlite3.Connection('flights.db')
c    = conn.cursor()
c.execute('DROP TABLE IF EXISTS tb')
c.execute('''
    CREATE TABLE IF NOT EXISTS tb 
      (
    légitársaság_kódja         TEXT,    -- carrier
    légitársaság_neve          TEXT,    -- carrier_name
    reptér_kódja               TEXT,    -- airport
    reptér_neve                TEXT,    -- airport_name
    érkező_járatok_száma       INTEGER, -- arr_flights
    késett_járatok_száma       INTEGER, -- arr_del15
    késések_összesítve_percben INTEGER, -- arr_delay
    törölt_járatok_száma       INTEGER  -- arr_cancelled
      )
''')
conn.commit()

def csv2sql():
    with open('flights_2.csv') as f:
        fejléc =  f.readline().strip().split(';')
        m = { mező_név.lstrip() : i for i, mező_név in enumerate(fejléc) }
        for sor in f:
            s = sor.strip().split(';')
            c.execute( "INSERT INTO tb VALUES (?,?,?,?,?,?,?,?) ",
                        ( s[ m['carrier'         ] ], # légitársaság_kódja
                          s[ m['carrier_name'    ] ], # légitársaság_neve,
                          s[ m['airport'         ] ], # reptér_kódja,
                          s[ m['airport_name'    ] ], # reptér_neve,
                          s[ m['arr_flights'     ] ], # érkező_járatok_száma,
                          s[ m['arr_del15'       ] ], # késett_járatok_száma,
                          s[ m['arr_delay'       ] ], # késések_összesítve_percben
                          s[ m['arr_cancelled'   ] ]  # törölt_járatok_száma
                        )
                      )
    conn.commit()    
csv2sql()

# legitarsasagok.txt 
c.execute('SELECT légitársaság_neve FROM tb GROUP BY légitársaság_neve')
légitársaságok = c.fetchall()
with open('legitarsasagok_listaja.txt','w') as f:
    [ print(sor[0], file=f ) for sor in légitársaságok ]

átlagos_késések = []
f = open('legitarsasag.txt', 'w')
txt ='****************************  Légitársaság ***************************************\n'
for társaság in légitársaságok:
    légitársaság = társaság[0]
    c.execute( 'SELECT  SUM(érkező_járatok_száma)  FROM tb  WHERE légitársaság_neve LIKE ?', (légitársaság,))
    összes_járat_száma = int( c.fetchall()[0][0] )
    txt += f'{légitársaság}                                                             \n'
    txt += f'               Az összes járat:             {összes_járat_száma}            \n'
  
    c.execute( 'SELECT  reptér_kódja FROM tb WHERE légitársaság_neve LIKE ?  GROUP BY reptér_kódja', (légitársaság,))
    repterek = c.fetchall()
    txt += f'               A látogatott repterek száma: { len(repterek)}                \n'
    
    c.execute( 'SELECT SUM(törölt_járatok_száma) FROM tb WHERE légitársaság_neve LIKE ? ', (légitársaság,))
    törölt_járatok_száma = int( c.fetchall()[0][0] )
    arány =  törölt_járatok_száma / összes_járat_száma
    txt += f'               A törölt járatok aránya:     {arány*100:.2f}%                 \n'
    
    c.execute( 'SELECT SUM(késések_összesítve_percben) FROM tb WHERE légitársaság_neve LIKE ? ', (légitársaság,))
    átlagos_járat_késés = int( c.fetchall()[0][0] )/összes_járat_száma
    txt += f'               Az átlagos járat késés:      {átlagos_járat_késés:.1f} perc    \n' 
    átlagos_késések.append( (átlagos_járat_késés, légitársaság))
 
    c.execute( 'SELECT SUM(érkező_járatok_száma),reptér_kódja  FROM tb WHERE légitársaság_neve LIKE ? GROUP BY reptér_kódja', (légitársaság,))
    reptér_forgalom, reptér_kód = max( c.fetchall() )
    txt += f'               A legforgalmasabb reptér:    {reptér_kód}   {reptér_forgalom}  \n'
    txt += f'------------------------------------------------------------------------------\n'
print( txt         )
print( txt, file=f )
f.close()


# 3 Legforgalmasabb Reptér 
c.execute( 'SELECT SUM(érkező_járatok_száma), reptér_neve, reptér_kódja  FROM tb  GROUP BY reptér_neve ORDER By SUM(érkező_járatok_száma) DESC')
repterek_forgalma = c.fetchall()

# with open('repterek.txt','w') as f:
#     txt      = f'                                                                 \n\n'
#     txt     += f'************* Repterek: 3 Legforgalmasabb Reptér ****************\n\n' 
#     for i in range(3):
#         txt += f'{i+1}. reptér: {repterek_forgalma[i][1] }                          \n'
#         txt += f'           Az összes járat: {repterek_forgalma[i][0]}              \n'
#         txt += f'           Kód:             {repterek_forgalma[i][2]}              \n'
#         x = search( query=(repterek_forgalma[i][2]+ 'Airport coordinate latlong.net' ), tld='co.in', lang='en', num=2, stop=1, pause=2)
#         txt += f'   koordináta:                                                     \n'
#         txt += f'                {list(x).pop()}                                  \n\n' 
#     print( txt         )
#     print( txt, file=f )
    
with open('kesesek.txt','w') as f:
    txt      = f'                                                                 \n\n'
    txt     += f'************* Késések:  3 legkisebb átlagos késés ***************\n\n' 
    for i in range(3):
        txt += f'{i+1}. társaság:  { átlagos_késések[i][1] }                        \n'
        txt += f'           Átlagos késés: { átlagos_késések[i][0]:.1f} perc        \n'
        txt += f' ------------------------------------------------------------------\n'
    print( txt         )
    print( txt, file=f )

légitársaságok_= [ sor[0].replace(' ','_') for sor in légitársaságok]

légitársaságok_szöveg_blokk = ''
for i in range(len(légitársaságok_)):
    légitársaságok_szöveg_blokk += f'''             <li><a href="{légitársaságok_[i]}.html">{légitársaságok[i][0]}</a></li>\n'''



légitársaságok_listája_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Légitársaságok Listája</title>
    <link rel="stylesheet" href="style.css" type="text/css">
</head>
<body>
    <div id="fejlec">
        Légitársaságok Listája
    </div>

    <div id="tartalom">
        <a href="index.html">Főoldal</a> > <a href="legitarsasagok_listaja.html">Légitársaságok Listája</a>
        <ul>
''' + légitársaságok_szöveg_blokk + '''
        </ul>
    </div>
</body>
</html>
'''
with open('legitarsasagok_listaja.html','w') as f:
    f.write(légitársaságok_listája_html)
