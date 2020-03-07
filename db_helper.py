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
    test_data = [
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-06-13', '2020-06-17', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 32500, '2020-03-13', '2020-03-17', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 32500, '2020-03-14', '2020-03-18', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 32500, '2020-03-20', '2020-03-24', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 32500, '2020-03-21', '2020-03-25', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 32500, '2020-03-27', '2020-03-31', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 32500, '2020-03-28', '2020-04-01', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-04-11', '2020-04-15', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-04-17', '2020-04-21', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-04-18', '2020-04-22', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-04-24', '2020-04-28', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-04-25', '2020-04-29', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 33000, '2020-05-02', '2020-05-06', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-05-08', '2020-05-12', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-05-09', '2020-05-13', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-05-15', '2020-05-19', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-05-16', '2020-05-20', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-05-22', '2020-05-26', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-05-23', '2020-05-27', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-05-29', '2020-06-02', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-05-30', '2020-06-03', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-06-05', '2020-06-09', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-06-06', '2020-06-10', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-06-12', '2020-06-16', 2, 10),
        ('歡樂關島~Royal Spa海陸主題遊5日', '92', 'VDR0000001925', 29900, '2020-06-13', '2020-06-17', 2, 10)]
    
    conn = sqlite3.connect('oop_prjdata_crawler.sqlite')
    cur = conn.cursor()
    cur.executemany('''INSERT OR IGNORE INTO EzTravel (title, travel_code, product_key, price, start_date, end_date, lower_bound, upper_bound)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', test_data)
    conn.commit()
    cur.close()

if __name__ == '__main__':  
    
    testFunc()