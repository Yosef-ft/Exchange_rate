# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from RateScraper.items import FullExchangeItems, ExchangeItem

import datetime
import logging
from decimal import Decimal

class RatescraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## Clean prices
        price_keys = ['Buying', 'Selling']
        for price_key in price_keys:
            try:
                value = adapter.get(price_key)
                adapter[price_key] = value.replace('\xa0', '').strip()
                adapter[price_key] = value.replace('\n', '').strip()
                adapter[price_key] = value.replace('\t', '').strip()
            except:
                pass

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
        date_formats = [
            '%B %d, %Y',
            '%B %d,%Y',
            '%d %B, %Y',
            '%d %b, %Y',
            '%b %d, %Y',
            '%b %d,%Y',
            '%Y-%m-%d',
            '%B %d %Y',
            '%d/%m/%Y',
            '%d %b  %Y'
        ]        

        for date_format in date_formats:
            try:
                adapter['Date'] = datetime.datetime.strptime(Date_string, date_format)
            except:
                pass


        ## CurrencyCode --> Clean CurrencyCode 
        curr_code = adapter.get('CurrencyCode')

        adapter['CurrencyCode'] = adapter['CurrencyCode'].replace('1', '').strip()
        adapter['CurrencyCode'] = adapter['CurrencyCode'].replace('\n', '').strip()
        adapter['CurrencyCode'] = adapter['CurrencyCode'].replace('\t', '').strip()

        symbol_converter = {'US Dollar' : 'USD', 'Euro' : 'EUR', 'Pound Sterling' : 'GBP', 'Saudi Riyal' : 'SAR', 'UAE Dirham' : 'AED', 'Japanese Yen' : 'JPY', 'Kuwait Dinar' : 'KWD'}
        try:
            adapter['CurrencyCode'] = symbol_converter[curr_code]
        except:
            pass
        
        if '(' in curr_code:
            adapter['CurrencyCode'] = adapter['CurrencyCode'][-4:-1]

        adapter['CurrencyCode'] = adapter['CurrencyCode'].replace('\xa0', '')
        adapter['CurrencyCode'] = adapter['CurrencyCode'].strip().split()[0]
        adapter['CurrencyCode'] = adapter['CurrencyCode'].replace('.', '')


        return item
    
        

import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        # For transactions and cash rate
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


        # For cash rate only
        self.conn2 = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'Rates'
        )

        self.cur2 = self.conn2.cursor()

        self.cur2.execute("""
        CREATE TABLE IF NOT EXISTS rates(
            bank VARCHAR(255),
            Date DATETIME,
            CurrencyCode VARCHAR(255),
            Buying DECIMAL(10,4),
            Selling DECIMAL(10,4)
        )
        """)
        

    def process_item(self, item, spider):
        if isinstance(item, FullExchangeItems):
            self.process_full_exchange_item(item, spider)
        elif isinstance(item, ExchangeItem):
            self.process_exchange_item(item, spider)


    def process_full_exchange_item(self, item, spider):
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
                item["CashBuying"],
                item["CashSelling"],
                item["TransactionalBuying"],
                item["TransactionalSelling"]
            ))

            ## Execute insert of data into database
            self.conn.commit()
        else:
            logging.debug(">>>>>>>>>>>>>>>>>>>>_____________________<<<<<<<<<<<<<<<<<<<<<<<<")
            logging.debug(f"Data for bank '{item['bank']}' and date '{item['Date']}' already exists in the database. Skipping insertion.")
   




    def process_exchange_item(self, item, spider):
        self.cur2.execute("SELECT COUNT(*) FROM rates WHERE Date = %s AND bank = %s AND CurrencyCode = %s", (item["Date"], item["bank"], item['CurrencyCode']))
        count = self.cur2.fetchone()[0]

        if count == 0:
            self.cur2.execute(""" insert into rates (
                bank, 
                Date, 
                CurrencyCode, 
                Buying, 
                Selling
                ) values (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    )""", (
                item["bank"],
                item["Date"],
                item["CurrencyCode"],
                item["Buying"],
                item["Selling"]
            ))

            ## Execute insert of data into database
            self.conn2.commit()
        else:
            logging.debug(">>>>>>>>>>_____________________<<<<<<<<<<<<")
            logging.debug(f"Data for bank '{item['bank']}' and date '{item['Date']}' already exists in the database. Skipping insertion.")            
    




    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()   

        self.cur2.close()
        self.conn2.close()   

               


