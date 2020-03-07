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
                UNIQUE(product_key,start_date)
                )''')
    # cur.execute('''
    #             CREATE TABLE IF NOT EXISTS EzTravel_Searched_Key(
    #                 id INTEGER AUTOINCREMENT, 
    #                 depDateFrom TEXT, 
    #                 depDateTo TEXT,
    #                 travel_code TEXT,
    #                 page_number INTEGER
    #             )''')

    # cur.execute('''
    #             CREATE TABLE IF NOT EXISTS EzTravel_Url(
    #                 id INTEGER AUTOINCREMENT, 
    #                 retrieved INTEGER, 
    #                 title TEXT,
    #                 price INTEGER
    #             )''')
        

def save2EzTravel_db(retrieved_travel_datas):
    conn = sqlite3.connect('oop_prjdata_crawler.sqlite')
    cur = conn.cursor()

    cur.executemany('''INSERT OR IGNORE INTO EzTravel (title, travel_code, product_key, price, start_date, end_date, lower_bound, upper_bound)
                    VALUES (:title, :travel_code, :product_key, :price, :start_date, :end_date, :lower_bound, :upper_bound)''', retrieved_travel_datas)
    conn.commit()
    cur.close()

def save2Code_table(retrieved_code_datas):
    conn = sqlite3.connect('oop_prjdata_crawler.sqlite')
    cur = conn.cursor()

    cur.executemany('''INSERT OR IGNORE INTO EzTravel_Code (code, name)
                    VALUES (:code, :name)''', retrieved_code_datas)
    conn.commit()
    cur.close()