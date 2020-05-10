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
                          s[ m['arr_delay'       ] ], # késések_összesítve_percben)
                          s[ m['arr_cancelled'   ] ]  # törölt_járatok_száma
                        )
                      )
    conn.commit()    
csv2sql()

# légitársaságok.txt 
c.execute('SELECT légitársaság_neve FROM tb GROUP BY légitársaság_neve')
légitársaságok = c.fetchall()
with open('legitarsasagok.txt','w') as f:
    [ print(sor[0], file=f ) for sor in légitársaságok ]

# legforgalmasabb_repülőterek.txt
c.execute( 'SELECT SUM(érkező_járatok_száma), reptér_neve  FROM tb  GROUP BY reptér_neve ORDER By SUM(érkező_járatok_száma) DESC')
repterek_forgalma = c.fetchall()
with open('legforgalmasabb_repuloterek.txt','w') as f:
    [ print( repterek_forgalma[i][0], repterek_forgalma[i][1], file=f ) for i in range(3) ]

f = open('legitarsasagok_statisztika.txt', 'w')
print('*****************************************************************************')
for légitársaság in légitársaságok:
    print(légitársaság[0],':-----------------------------------------------------------')
    print(légitársaság[0],':-----------------------------------------------------------', file=f)
    c.execute( 'SELECT  SUM(érkező_járatok_száma)  FROM tb  WHERE légitársaság_neve LIKE ?', (légitársaság[0],))
    összes_járat_száma = int( c.fetchall()[0][0] )
    print(f'               Az összes járat:             {összes_járat_száma}')
    print(f'               Az összes járat:             {összes_járat_száma}', file=f)
    
    c.execute( 'SELECT  reptér_kódja FROM tb WHERE légitársaság_neve LIKE ?  GROUP BY reptér_kódja', (légitársaság[0],))
    repterek = c.fetchall()
    print(f'               A látogatott repterek száma: { len(repterek) }')
    print(f'               A látogatott repterek száma: { len(repterek) }', file=f)
    
    c.execute( 'SELECT SUM(törölt_járatok_száma) FROM tb WHERE légitársaság_neve LIKE ? ', (légitársaság[0],))
    törölt_járatok_száma = int( c.fetchall()[0][0] )
    arány =  törölt_járatok_száma / összes_járat_száma
    print(f'               A törölt járatok aránya:     {arány*100:.2f}%')
    print(f'               A törölt járatok aránya:     {arány*100:.2f}%', file=f)

f.close()