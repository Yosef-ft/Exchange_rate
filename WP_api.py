import requests
import base64
import json
import datetime
import mysql.connector


class Banks:
    def __init__(self):

        # For cash rate only
        self.conn2 = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'Rates' 
        )

        self.cur2 = self.conn2.cursor()  

        # For transactions and cash rate
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'FullRates'
        )

        self.cur = self.conn.cursor()



    def rate_table(self, bank: str) -> str:
        
        self.cur2.execute('SELECT * FROM rates WHERE bank = %s ORDER BY date DESC', (bank,))
        result = self.cur2.fetchall()
        most_recent_date = result[0][1]
        recent_rates = [rate for rate in result if rate[1] == most_recent_date]

        table_content = ''
        table_content += f'<!-- wp:heading --> <strong>{result[0][0]} bank </strong> exchange rate <!-- /wp:heading -->' + '<br>'
        table_content += 'Last updated, ' + result[0][1].strftime('%d/%m/%Y') + '<br>'
        table_content += '<table>'
        table_content += '<tr><th>Code</th><th>Buying</th><th>Selling</th></tr>'
        for rate in recent_rates:
            table_content += f'<tr><td>{rate[2]}</td><td>{rate[3]}</td><td>{rate[4]}</td></tr>'
        table_content += '</table>'

        return table_content
    
    def all_rate_table(self, bank: str) -> str:
        
        self.cur.execute('SELECT * FROM rates WHERE bank = %s ORDER BY date DESC', (bank,))
        result = self.cur.fetchall()
        most_recent_date = result[0][1]
        recent_rates = [rate for rate in result if rate[1] == most_recent_date]

        table_content = ''
        table_content += f'<!-- wp:heading --> <strong>{result[0][0]} bank </strong> exchange rate <!-- /wp:heading -->' + '<br>'
        table_content += 'Last updated, ' + result[0][1].strftime('%d/%m/%Y') + '<br>'
        table_content += '<table>'
        table_content += '<tr><th>Code</th><th>Cash Buying</th><th>Cash Selling</th><th>Transaction Buying</th><th>Transaction Selling</th></tr>'
        for rate in recent_rates:
            table_content += f'<tr><td>{rate[2]}</td><td>{rate[3]}</td><td>{rate[4]}</td><td>{rate[5]}</td><td>{rate[6]}</td></tr>'
        table_content += '</table>'

        return table_content

    def cash_banks_table(self):
        self.cur2.execute('select distinct bank from rates')
        banks = self.cur2.fetchall()
        banks = [bank[0] for bank in banks]     
        
        tables = []   

        for bank in banks:
            tables.append(self.rate_table(bank))

        return tables


    def TranCash_banks_table(self):
        self.cur.execute('select distinct bank from rates')
        banks = self.cur.fetchall()
        banks = [bank[0] for bank in banks] 

        tables = []

        for bank in banks:
            tables.append(self.all_rate_table(bank))

        return tables


def main():
    url = 'http://exchange-rates.local/wp-json/wp/v2'

    user = 'yosefetene01'
    password = 'vmC6 l3YK aE9i YA2O wLRj Tuqt'
    creds = user + ":" + password
    token = base64.b64encode(creds.encode())
    header = {'Authorization' : 'Basic ' + token.decode('utf-8')}

    Bank_DB = Banks()
    table_content = ' '.join(Bank_DB.TranCash_banks_table()) + ' '.join(Bank_DB.cash_banks_table())

    time_now = datetime.datetime.now().date().strftime('%Y-%m-%d')
    post = {
        'date' : time_now + 'T00:00:00',
        'title' : 'Exchange rates',
        'content' : table_content,
        'status' : 'publish'
    }

    r = requests.post(url + '/posts' , headers=header, json=post)
    print(r.json())
    print(r.status_code)


if __name__ == "__main__":
    main()