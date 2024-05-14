import sqlite3

# Connect to the SQLite database
file_path = 'C:/Users/haolin/Desktop/backtest/data/example/BTCUSDT_2024-05-02_books5.db'
conn = sqlite3.connect(file_path)
cursor = conn.cursor()



cursor.execute('''
    SELECT PRICE.TIMESTAMP, PRICE.LEVEL10, PRICE.LEVEL1, QUANTITY.LEVEL10, QUANTITY.LEVEL1
    FROM PRICE
    INNER JOIN QUANTITY ON PRICE.TIMESTAMP = QUANTITY.TIMESTAMP
''')
rows = cursor.fetchall()
for row in rows:
    timestamp = row[0]
    price_level10 = row[1]
    price_level1 = row[2]
    quantity_level10 = row[3]
    quantity_level1 = row[4]
    # Process or print the data as needed
    print(type(price_level10))


# Commit the transaction and close the connection


conn.close()