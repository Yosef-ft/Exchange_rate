# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import datetime
from decimal import Decimal

class RatescraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## Price --> convert to float
        price_keys = ['CashBuying', 'CashSelling', 'TransactionalBuying', 'TransactionalSelling']
        for price_key in price_keys:
            try:
                value = adapter.get(price_key)
                adapter[price_key] = Decimal(value)  
            except Exception as e:
                pass

        ## Date  --> convert to datetime
        Date_string = adapter.get('Date')
        try:
            adapter['Date'] = datetime.datetime.strptime(Date_string, '%B %d, %Y')
        except:
            adapter['Date'] = datetime.datetime.strptime(Date_string, '%b %d, %Y')
        

        ## Code --> remove \xa0 from currency code, display only currency code
        curr_code = adapter.get('CurrencyCode')
        adapter['CurrencyCode'] = adapter['CurrencyCode'].replace('\xa0', '')
        adapter['CurrencyCode'] = adapter['CurrencyCode'].strip().split()[0]


        return item
    
        

import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'FullRates'
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS rates(
            bank VARCHAR(255),
            Date DATETIME,
            CurrencyCode VARCHAR(255),
            CashBuying DECIMAL(10,4),
            CashSelling DECIMAL(10,4),
            TransactionalBuying DECIMAL(10,4),
            TransactionalSelling DECIMAL(10,4)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute("SELECT COUNT(*) FROM rates WHERE Date = %s AND bank = %s AND CurrencyCode = %s", (item["Date"], item["bank"], item['CurrencyCode']))
        count = self.cur.fetchone()[0]

        if count == 0:
            self.cur.execute(""" insert into rates (
                bank, 
                Date, 
                CurrencyCode, 
                CashBuying, 
                CashSelling,
                TransactionalBuying,
                TransactionalSelling
                ) values (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    )""", (
                item["bank"],
                item["Date"],
                item["CurrencyCode"],
                float(item["CashBuying"]),
                float(item["CashSelling"]),
                item["TransactionalBuying"],
                item["TransactionalSelling"]
            ))

            ## Execute insert of data into database
            self.conn.commit()
        else:
            print(">>>>>>>>>>_____________________<<<<<<<<<<<<")
            print(f"Data for bank '{item['bank']}' and date '{item['Date']}' already exists in the database. Skipping insertion.")
    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()          