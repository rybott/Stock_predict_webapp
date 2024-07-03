import duckdb as ddb

con = ddb.connect('OptionsTrading.duckdb')

class DBconn():
    def __init__(self):
        con.execute('''
        CREATE TABLE IF NOT EXISTS Options (
            contractID VARCHAR,
            symbol VARCHAR,
            expiration VARCHAR,
            strike FLOAT,
            type VARCHAR,
            last FLOAT,
            mark FLOAT,
            bid FLOAT,
            bid_size FLOAT,
            ask FLOAT,
            ask_size FLOAT,
            volume FLOAT,
            open_interest FLOAT,
            date VARCHAR,
            Logtime TIMESTAMP
        )''')

        con.execute('''
        CREATE TABLE IF NOT EXISTS Stocks (
            Timestamp TIMESTAMP,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume FLOAT
        )''')

    
    def InsertOptionQry(df):
        con.register('df', df)
        con.execute(
            '''
            INSERT INTO Options
            SELECT 
                contractID,
                symbol,
                expiration,
                strike,
                type,
                last,
                mark,
                bid,
                bid_size,
                ask,
                ask_size,
                volume,
                open_interest,
                date,
                CAST(Logtime as TIMESTAMP) as Logtime
            FROM df
            WHERE Logtime NOT IN (SELECT Logtime FROM Options)
            ''')
    
    def InsertStockQry(df):
        con.register('df', df)
        con.execute(
            '''
            INSERT INTO Stocks
            SELECT 
                Timestamp,
                "1. open" as open,
                "2. high" as high,
                "3. low" as low, 
                "4. close" as close, 
                "5. volume" as volume
            FROM df
            WHERE Timestamp NOT IN (SELECT Timestamp FROM Stocks)
            ''')
    