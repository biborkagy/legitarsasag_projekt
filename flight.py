# pip3 install beautifulsoup4
# pip3 install google

def légitársaságok_nevei():
    from googlesearch import search

    with open('flights.csv') as f:
        fejléc =  f.readline()
        lista  =  [ sor.strip().split(',') for sor in f]
    
    légitársaságok   = sorted(list( { sor[3] for sor in lista } ))

    for  légitársaság in légitársaságok:
        for j in search(légitársaság, num=1, stop=1, pause=3 ):
            print(légitársaság, j) 
    print('------------------------------')
#-------------------------------------------------------------------------------------------------------------------------------------------
#fejléc
#'"year"," month","carrier","carrier_name","airport","airport_name","arr_flights","arr_del15","carrier_ct"," weather_ct","nas_ct","security_ct","late_aircraft_ct","arr_cancelled","arr_diverted"," arr_delay"," carrier_delay","weather_delay","nas_delay","security_delay","late_aircraft_delay",\n'

import sqlite3
conn = sqlite3.Connection('flights.db')
c = conn.cursor()

'''
carrier: A légitársaság kódja
carrier_name: A légitársaság neve
airport: A reptér kódja
airport_name: A reptér neve
arr_flights: Az érkező járatok száma
arr_del15: A késett járatok száma
arr_delay: A késések összesítve percben

'"year", " month", "carrier," "carrier_name", "airport",
"airport_name", "arr_flights", "arr_del15", "carrier_ct", " weather_ct",
"nas_ct", "security_ct", "late_aircraft_ct", "arr_cancelled" "arr_diverted",
" arr_delay"," carrier_delay","weather_delay","nas_delay", "security_delay",
"late_aircraft_delay",'
'''

c.execute('''
    CREATE TABLE IF NOT EXISTS tb 
      (
    carrier       TEXT,
    carrier_name  TEXT,
    airport       TEXT,
    airport_name  TEXT,
    arr_flights   INTEGER,
    arr_del15     INTEGER,
    arr_delay     INTEGER
      )
''')
conn.commit()

def db_feltöltés():
    with open('flights.csv') as f:
        fejléc =  f.readline()
        for sor in f:
            s = sor.strip().split(',')
            carrier, carrier_name, airport, airport_name, arr_flights, arr_del15, arr_delay = s[2], s[3], s[4], s[5], s[6], s[7], s[15]
            c.execute(" INSERT INTO tb VALUES (?,?,?,?,?,?,?) ", ( carrier, carrier_name, airport, airport_name, arr_flights, arr_del15, arr_delay )  ) 
    conn.commit()
    
# Légitársaságok:
c.execute('SELECT carrier_name FROM tb GROUP BY carrier_name')
légitársaságok = c.fetchall()



