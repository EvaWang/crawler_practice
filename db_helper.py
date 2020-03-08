import sqlite3

def init_database():
    conn = sqlite3.connect('oop_prjdata_crawler.sqlite')
    cur = conn.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS EzTravel_Code
                (id INTEGER PRIMARY KEY, 
                code TEXT NOT NULL UNIQUE, 
                name TEXT NOT NULL
                )''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS EzTravel
                (id INTEGER PRIMARY KEY, 
                title TEXT NOT NULL, 
                travel_code TEXT NOT NULL,
                product_key TEXT NOT NULL, 
                price INTEGER NOT NULL, 
                start_date TEXT NOT NULL, 
                end_date TEXT NOT NULL,
                lower_bound INTEGER NOT NULL,
                upper_bound INTEGER NOT NULL,
                UNIQUE(travel_code,product_key,start_date)
                )''')
        
def save2EzTravel_db(retrieved_travel_datas):
    conn = sqlite3.connect('oop_prjdata_crawler.sqlite')
    cur = conn.cursor()

    cur.executemany('''INSERT OR IGNORE INTO EzTravel (title, travel_code, product_key, price, start_date, end_date, lower_bound, upper_bound)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', retrieved_travel_datas)
    conn.commit()
    cur.close()

def save2Code_table(retrieved_code_datas):
    conn = sqlite3.connect('oop_prjdata_crawler.sqlite')
    cur = conn.cursor()

    cur.executemany('''INSERT OR IGNORE INTO EzTravel_Code (code, name)
                    VALUES (:code, :name)''', retrieved_code_datas)
    conn.commit()
    cur.close()

def testFunc():
    test_data = [{'product_key': 'pkgfrn', 'start_date': '2020-04-14', 'end_date': '2020-04-17', 'lower_bound': 1, 'upper_bound': 10, 'title': '*【親子關島】PIC水陸玩透透、童趣安可魔術秀、披薩DIY、生態浮潛追海豚、海龜浮潛 4天', 'price': '28500', 'travel_code': '92'}]
    
    conn = sqlite3.connect('oop_prjdata_crawler.sqlite')
    cur = conn.cursor()
    cur.executemany('''INSERT OR IGNORE INTO EzTravel (title, travel_code, product_key, price, start_date, end_date, lower_bound, upper_bound)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', test_data)
    conn.commit()
    cur.close()

if __name__ == '__main__':  
    
    testFunc()