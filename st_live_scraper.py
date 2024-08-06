import scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx

import threading
import datetime
import os
import sys

import pandas as pd
import json

def reboot_app():
    """Restarts the current Streamlit app"""
    os.execl(sys.executable, sys.executable, *["st_live_scraper.py"] + sys.argv[1:])
    # os.execl(sys.executable, sys.executable, *sys.argv)


st.set_page_config(layout="wide")
st.button("Reboot App", on_click=reboot_app)
st.title('Exchange Rate')

st.header('List of Currency rates')

def display_data(data):
    df = pd.DataFrame(data)
    df.dropna(inplace=True)


    date = df['Date'][0]
    bank = df['bank'][0]

    df.drop(['bank', 'Date'], axis = 1, inplace = True)

    df.set_index('CurrencyCode', inplace=True)

    with st.expander(f'{bank} bank exchange rate'):
        st.write('Last updated', date)
        st.write(df)

class AbaySpider(scrapy.Spider):
    name = "Abay"
    allowed_domains = ["abaybank.com.et"]
    start_urls = ["https://abaybank.com.et/exchange-rates/"]

    def __init__(self):
        self.data = []

    def parse(self, response):
        Rates = response.css('tbody.row-hover tr')

        for rate in Rates:
            self.data.append({
                'bank' : self.name,
                'Date': response.css('table tr th.column-1::text').get(),
                'CurrencyCode': rate.css('td.column-1::text').get().strip(),
                'Buying': rate.css('tr td.column-2::text').get(),
                'Selling': rate.css('td.column-3::text').get(),
            })

        display_data(self.data)

        
    

class AddisSpider(scrapy.Spider):
    name = "Addis"
    allowed_domains = ["addisbanksc.com"]
    start_urls = ["https://addisbanksc.com/exchange-rate/"]

    def __init__(self):
        self.data = []    

    def parse(self, response):
        
        data =  response.css('table tbody tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []        

        for rate in Rates:
            self.data.append({
                'bank' : self.name,
                'Date' : response.css('tfoot tr th.column-2::text').get(),
                'CurrencyCode': rate[0],
                'Buying': rate[1],
                'Selling': rate[2],
            })

        display_data(self.data)

        
    

class AhaduSpider(scrapy.Spider):
    name = "Ahadu"
    allowed_domains = ["ahadubank.com"]
    start_urls = ["https://ahadubank.com/"]


    def __init__(self):
        self.data = []        

    def parse(self, response):
        
        symbols = response.css('div.elementor-icon-box-content h6 span::text').getall()
        prices = response.css('div.elementor-icon-box-content p::text').getall()
        prices = prices[2:]
        prices =[rate.split(':')[1] for rate in prices]

        Rates = []
        for sym in symbols:
            temp = [sym]
            counter = 0
            for price in prices[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)           

        for rate in Rates:
            self.data.append({            
            'bank': self.name,
            "Date": response.css('div.elementor-widget-container h5.litho-heading span.litho-primary-title ::text').getall()[-1]  ,
            "CurrencyCode": rate[0],
            "Buying":rate[1],
            "Selling" : rate[2],
            })

        display_data(self.data)

             


class AmharaSpider(scrapy.Spider):
    name = "Amhara"
    allowed_domains = ["www.amharabank.com.et"]
    start_urls = ["https://www.amharabank.com.et/exchange-rate/"]


    def __init__(self):
        self.data = []            

    def parse(self, response):
        
        data = response.css('table tbody tr td div span span::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []          

        day_month = response.css('div.elementor-widget-container p::text').getall()[5]
        day_month= day_month.split()[-2:]
        day_month = ' '.join(day_month)
        year = response.css('div.elementor-widget-container p span::text').get()[:-1]
        Date = day_month + year

        for rate in Rates:
            self.data.append({  
                'bank': self.name,
                'Date': Date,
                'CurrencyCode': rate[0],
                'Buying': rate[1],
                'Selling': rate[2],

            })

        display_data(self.data)

             
    

class BerhanSpider(scrapy.Spider):
    name = "Berhan"
    allowed_domains = ["berhanbanksc.com"]
    start_urls = ["https://berhanbanksc.com/exchange-rates/"]

    def __init__(self):
        self.data = []            
    

    def parse(self, response):
        
        prices = response.css('div.row div.col-3::text').getall()
        prices = prices[2:]
        prices = [price.strip() for price in prices]

        symbols = response.css('div.row div.col-6 span::text').getall()
        symbols = [symbol.strip().split()[1] for symbol in symbols if symbol.strip() != '']

        Rates = []
        for sym in symbols:
            temp = [sym]
            counter = 0
            for price in prices[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)        

        for rate in Rates:
            self.data.append({  
                'bank': self.name,
                "Date": response.css('div.innerContainer h3::text').get().strip(),
                "CurrencyCode": rate[0],
                "Buying":rate[1],
                "Selling": rate[2],
            })

        display_data(self.data)

             

class AwashSpider(scrapy.Spider):
    name = "Awash"
    allowed_domains = ["awashbank.com"]
    start_urls = ["https://awashbank.com/exchange-historical/"]

    
    def __init__(self):
        self.data = []            


    def parse(self, response):
        
        Rates = response.css('table tbody tr')
        Ind_Rates = [rate.css('td::text').getall() for rate in Rates]

        for rate in Ind_Rates:
            self.data.append({  
                'bank': 'Awash',
                'Date':response.css('div.exchange-rates-header span::text').get(),
                'CurrencyCode': rate[0],
                'CashBuying': rate[1],
                'CashSelling': rate[2],
                'TransactionalBuying': rate[3],
                'TransactionalSelling': rate[4],
            
            })

        display_data(self.data)

             


class BoaSpider(scrapy.Spider):
    name = "BOA"
    allowed_domains = ["www.bankofabyssinia.com"]
    start_urls = ["https://www.bankofabyssinia.com"]

    
    def __init__(self):
        self.data = []            

    def parse(self, response):
        
        Rates = response.css('table tbody tr')
        Ind_rates = [rate.css('td ::text') for rate in Rates]

        all_data = []

        for rate in Ind_rates:
            all_data.append(rate.getall())


        cash_data = []
        
        for rate in Ind_rates:
            if 'Transaction' in ' '.join(rate.getall()):
                break
            cash_data.append(rate.getall())
        

        trans_data = all_data[len(cash_data):]
        trans_data = trans_data[2:]
        trans_data = trans_data[:-1]

        cash_data = cash_data[2:]

        trans_common = [row for row in trans_data if row[0] in [r[0] for r in cash_data]]
        
        cash_common = [row for row in cash_data if row[0] in [r[0] for r in trans_data]]
        cash_common = sorted(cash_common)
        trans_common = sorted(trans_common)


        for i in range(len(cash_common)):
            self.data.append({  
                'bank':"Abyssinia",
                'Date': response.css('table tr th.column-1::text').get(),
                'CurrencyCode': cash_common[i][0],
                'CashBuying':cash_common[i][1],
                'CashSelling': cash_common[i][2],
                'TransactionalBuying': trans_common[i][1],
                'TransactionalSelling': trans_common[i][2],
            })

        display_data(self.data)

             


class BunnaSpider(scrapy.Spider):
    name = "Bunna"
    allowed_domains = ["bunnabanksc.com"]
    start_urls = ["https://bunnabanksc.com/"]

    
    def __init__(self):
        self.data = []          
  
    def parse(self, response):
        
        data = response.css('table tbody tr td div span::text').getall()
        data = [rate.replace('\t', '').replace('\n','') for rate in data]
        data = [rate for rate in data if rate != ' ' and rate != '' ]

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 5:
                Rates.append(temp)
                temp = []             
                    

        ## Constantly changing their website this is just half the data
        for rate in Rates:
            self.data.append({             
            'bank': self.name,
            'Date': response.css('div.elementor-element div.elementor-widget-container h4::text').get(),
            'CurrencyCode': rate[0],
            'CashBuying':rate[1],
            'CashSelling': rate[2],
            'TransactionalBuying': rate[3],
            'TransactionalSelling': rate[4] ,

            })

        display_data(self.data)

             
    

class CbeSpider(scrapy.Spider):
    name = "CBE"
    allowed_domains = ["combanketh.et"]
    start_urls = ["https://combanketh.et"]

    headers = {
        "accept" : "application/json, text/plain, */*",
        "accept-encoding" : "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "referer" : "https://combanketh.et/en/exchange-rate/",
        "sec-fetch-mode" : "cors",
        "sec-fetch-site" : "same-origin",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "X-Requested-With" : "Fetch"
    }

    def __init__(self):
        self.data = []              

    def parse(self, response):
        # url = 'https://combanketh.et/cbeapi/daily-exchange-rates?_limit=1&_sort=Date%3ADESC'

        url = 'https://combanketh.et/cbeapi/daily-exchange-rates/?_limit=1&Date='

        date = datetime.datetime.now()

        # for day in range(0, 31):
        #     hist_date = (date - datetime.timedelta(days=day))
        #     if hist_date.weekday() == 5 or hist_date.weekday() == 6:
        #         continue
        #     else:
        #         hist_date = (date - datetime.timedelta(days=day)).strftime('%Y-%m-%d')

        today_url = 'https://combanketh.et/cbeapi/daily-exchange-rates?_limit=1&_sort=Date%3ADESC'
        request = scrapy.Request(url = today_url,
                                callback= self.parse_api,
                                headers = self.headers)
        
        yield request


    
    def parse_api(self, response):
        
        raw_data = response.body
        data = json.loads(raw_data)[0]

        for rate in data['ExchangeRate']:
            self.data.append({      
            'bank': 'CBE',
            'Date': data['Date'],
            'CashBuying': rate['cashBuying'],
            'CashSelling': rate['cashSelling'],
            'TransactionalBuying':rate['transactionalBuying'],
            'TransactionalSelling': rate['transactionalSelling'],
            'CurrencyCode': rate['currency']['CurrencyCode'],
            
            })

        display_data(self.data)

             
    
class CoopSpider(scrapy.Spider):
    name = "Coop"
    allowed_domains = ["coopbankoromia.com.et"]
    start_urls = ["https://coopbankoromia.com.et/daily-exchange-rates/"]

    def __init__(self):
        self.data = []              


    def parse(self, response):
       
        data = response.css('table tbody tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 5:
                Rates.append(temp)
                temp = []       

        for rate in Rates:
            self.data.append({  
            'bank': self.name,
            'Date': response.css('div.exchange-rates-header h4 span::text').get(),
            'CurrencyCode': rate[0],
            'CashBuying':rate[1],
            'CashSelling': rate[2],
            'TransactionalBuying': rate[3],
            'TransactionalSelling': rate[4] ,       
           
            })

        display_data(self.data)

             
    

class DashenSpider(scrapy.Spider):
    name = "Dashen"
    allowed_domains = ["dashenbanksc.com"]
    start_urls = ["https://dashenbanksc.com"]

    def __init__(self):
        self.data = []              


    def parse(self, response):
        
        data = response.css('table tr td::text').getall()
        
        # Rates include symbol, buying and selling both cash and transaction but duplicated
        temp = []
        Rates = []
        for i in range(0, len(data), 4):
            temp.append(data[i])
            temp.append(data[i+1])
            temp.append(data[i+2])
            temp.append(data[i+3])
            if len(temp) == 4:
                Rates.append(temp)
                temp = []

        Rates = sorted(Rates)

        # The duplicated rates
        dup_Rates = []
        for i in range(0, len(Rates)-1):
            if Rates[i][0] == Rates[i + 1][0]:
                dup_Rates.append(Rates[i])
                dup_Rates.append(Rates[i+1])

        # Joins the Duplicated rates
        Dup_Rates = []
        for i in range(0, len(dup_Rates), 2):
            Dup_Rates.append(dup_Rates[i] + dup_Rates[i+1])

        # Rates that are not duplicated i.e, rates that don't have trasaction rates
        single_rates = [rate for rate in Rates if rate[0] not in [r[0] for r in dup_Rates]]

        # One rate includes the cash and trasaction rates for the duplicated rates
        main_rate = []
        one_rate = []
        for rate in Dup_Rates:
            main_rate.append(rate[0])
            main_rate.append(rate[1])
            main_rate.append(rate[2])
            main_rate.append(rate[3])
            main_rate.append(rate[6])
            main_rate.append(rate[7])
            if len(main_rate) == 6:
                one_rate.append(main_rate)
                main_rate = []

        total_rates = one_rate + single_rates

        for rate in total_rates:
            try:
                self.data.append({  
                    'bank':self.name,
                    'Date':response.css('div.et_pb_text_inner h4::text').get()[14:],
                    'CurrencyCode':rate[0],
                    'CashBuying':rate[2],
                    'CashSelling':rate[3],
                    'TransactionalBuying':rate[4],
                    'TransactionalBuying':rate[2],
                    'TransactionalSelling':rate[5],
                    'TransactionalSelling':rate[3],    
                })
            except:
                pass

        display_data(self.data)

            


class DebubGlobalSpider(scrapy.Spider):
    name = "Debub_Global"
    allowed_domains = ["www.globalbankethiopia.com"]
    start_urls = ["https://www.globalbankethiopia.com"]


    def __init__(self):
        self.data = []          

    def parse(self, response):
        
        data = response.css('table tr td div div p::text').getall()
        symbol = response.css('table tr td div div p strong::text').getall()
        symbol = symbol[3:]

        Rates = []
        for sym in symbol:
            temp = [sym]
            counter = 0
            for price in data[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)


        for rate in Rates:
            self.data.append({  
            'bank':"Debub Global",
            "Date": response.css('div.elementor-shortcode ::text').get(),
            "CurrencyCode":rate[0],
            "Buying":rate[1],
            "Selling":rate[2],

                })


        display_data(self.data)

            
    
class EnatSpider(scrapy.Spider):
    name = "Enat"
    allowed_domains = ["www.enatbanksc.com"]
    start_urls = ["https://www.enatbanksc.com"]


    def __init__(self):
        self.data = []        

    def parse(self, response):
        
        datas = response.css('tbody tr td::text').getall()
        datas = [data for data in datas if data != '\n']


        rates = []
        temp = []
        for i in range(0, len(datas)):
            temp.append(datas[i])
            try:
                float(datas[i+1])
                temp.append(datas[i+1])
                temp.append(datas[i+2])
                rates.append(temp)
            except:
                temp = []


        dup_Rates = []
        for rate in rates:
            dup_Rates.append(rate[:3])


        Rates = []
        for i in range(0, len(dup_Rates), 2):
            Rates.append(dup_Rates[i])

        
        for rate in Rates:
            self.data.append({  
            'bank':self.name,
            'Date':response.css('div.et_pb_text_inner h1.p1 strong::text').get().split()[-1],
            "CurrencyCode":rate[0],
            "Buying":rate[1],
            "Selling":rate[2] ,

                })

        display_data(self.data)

           
    

class GadaaSpider(scrapy.Spider):
    name = "Gadaa"
    allowed_domains = ["www.gadaabank.com.et"]
    start_urls = ["https://www.gadaabank.com.et/"]

    def __init__(self):
        self.data = []        


    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()
        data = data[4:]

        Rates = []
        temp = []
        for i in range(0, len(data) - 4, 4):
            temp.append(data[i])
            temp.append(data[i+1])
            temp.append(data[i+2])
            Rates.append(temp)
            temp = []

        Rates = Rates[:(len(Rates) //2)]

        for rate in Rates:
            self.data.append({  
                'bank':self.name,
                'Date':response.css('div.elementor-shortcode p.wpdt-c::text').get()[:-14],
                'CurrencyCode':rate[0],
                'Buying':rate[1],
                'Selling':rate[2],

                })

        display_data(self.data)

           
    

class GohBetochSpider(scrapy.Spider):
    name = "Goh_Betoch"
    allowed_domains = ["www.gohbetbank.com"]
    start_urls = ["https://www.gohbetbank.com/exchange-rate/"]

    
    def __init__(self):
        self.data = []        

    def parse(self, response):
        
        symbols = response.css('table tr td p strong::text').getall()
        prices = response.css('table tr td p::text').getall()
        prices = [price for price in prices if price != ' ']

        Rates = []
        temp = []
        for rate in prices:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []  

        for i in range(0, len(Rates)):
            Rates[i][0]= symbols[i]

        for rate in Rates:
            self.data.append({  
                'bank':"Goh Betoch",
                'Date':response.css('div.elementor-widget-container p::text').getall()[1][14:],
                'CurrencyCode':rate[0],
                'Buying':rate[1],
                'Selling':rate[2],


                })

        display_data(self.data)

                     
    
class HibretSpider(scrapy.Spider):
    name = "Hibret"
    allowed_domains = ["www.hibretbank.com.et"]
    start_urls = ["https://www.hibretbank.com.et/"]

    
    def __init__(self):
        self.data = []        

    def parse(self, response):
        
        data =  response.css('table tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []  

        for rate in Rates:
            self.data.append({  
                'bank':self.name,
                'Date':response.css('table tr th::text').get(),
                'CurrencyCode':rate[0],
                'Buying':rate[1],
                'Selling':rate[2],
                })

        display_data(self.data)

               

class HijraSpider(scrapy.Spider):
    name = "Hijra"
    allowed_domains = ["hijra-bank.com"]
    start_urls = ["https://hijra-bank.com/"]

    def __init__(self):
        self.data = []       

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 5:
                Rates.append(temp)
                temp = []          

        for rate in Rates:
            self.data.append({  
                'bank':self.name,
                'Date':response.css("meta[property='article:modified_time']::attr(content)").get()[:10],
                'CurrencyCode':rate[0],
                'CashBuying' : rate[1],
                'CashSelling':rate[2],
                'TransactionalBuying':rate[3],
                'TransactionalSelling':rate[4]  ,
            
                })

        display_data(self.data)

                   

class NbeSpider(scrapy.Spider):
    name = "NBE"
    allowed_domains = ["api.nbe.gov.et"]
    start_urls = ["https://api.nbe.gov.et/api/filter-transaction-exchange"]


    def __init__(self):
        self.data = []          

    def parse(self, response):
        
        raw_data = response.body
        data = json.loads(raw_data)

        price_data = data['data']

        for rate in price_data: 
            self.data.append({  
                'bank':self.name,
                'Date':rate['date'],
                "CurrencyCode":rate['currency']['code'],
                "Buying":rate['buying'],
                "Selling":rate['selling'] ,
                })

        display_data(self.data)

                   
    

class NibSpider(scrapy.Spider):
    name = "Nib"
    allowed_domains = ["www.nibbanksc.com"]
    start_urls = ["https://www.nibbanksc.com"]

    def __init__(self):
        self.data = []          


    def parse(self, response):
        
        data = response.css('table.ea-advanced-data-table tbody tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 5:
                Rates.append(temp)
                temp = []

        for rate in Rates:
            self.data.append({  
                'bank':self.name,
                'Date':response.css('table thead tr th::text').get(),
                'CurrencyCode':rate[0],
                'CashBuying' : rate[1],
                'CashSelling':rate[2],
                'TransactionalBuying':rate[3],
                'TransactionalSelling':rate[4]  ,
                })

        display_data(self.data)

            


class OromiaSpider(scrapy.Spider):
    name = "Oromia"
    allowed_domains = ["www.ob.oromiabank.com"]
    start_urls = ["https://www.ob.oromiabank.com"]

    def __init__(self):
        self.data = []     

    def parse(self, response):
       
        symbol_src = response.css('table tbody tr td img::attr(src)').extract()

        symbols = []
        for sym in symbol_src:
            symbols.append(sym.split('1.png')[0][-3:])

        prices = response.css('table tbody tr td::text').getall()
        prices = prices[2:] 

        Rates = []
        for sym in symbols:
            temp = [sym]
            counter = 0
            for price in prices[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)       

        for rate in Rates:
            self.data.append({  
            'bank':self.name,
            "Date": response.css('figcaption.wp-element-caption code::text').get(),
            "CurrencyCode":rate[0],
            "Buying":rate[1],
            "Selling":rate[2],
                })

        display_data(self.data)

            

           
class SiinqeeSpider(scrapy.Spider):
    name = "Siinqee"
    allowed_domains = ["siinqeebank.com"]
    start_urls = ["https://siinqeebank.com/#/"]

    def __init__(self):
        self.data = []     

    def parse(self, response):
        
        data = response.css('table tr td::text').getall()

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 3:
                Rates.append(temp)
                temp = []  

        ## The website doesn't provide when the data has been updated
        now = datetime.datetime.now()
        date_string = now.strftime('%B %d, %Y')                

        for rate in Rates:
            self.data.append({  
                'bank':self.name,
                'Date':date_string,
                'CurrencyCode':rate[0],
                'Buying':rate[1],
                'Selling':rate[2],
                })

        display_data(self.data)

            


class TsedeySpider(scrapy.Spider):
    name = "Tsedey"
    allowed_domains = ["tsedeybank-sc.com"]
    start_urls = ["https://tsedeybank-sc.com/"]

    def __init__(self):
        self.data = []     

    def parse(self, response):
        
        symbols = response.css('table tbody tr td div div div h4::text').getall()
        prices = response.css('table tbody tr td div div p::text').getall()

        Rates = []
        for sym in symbols:
            temp = [sym]
            counter = 0
            for price in prices[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)          

        ## The website doesn't provide when the data has been updated
        now = datetime.datetime.now()
        date_string = now.strftime('%B %d, %Y')

        for rate in Rates:
            self.data.append({  
                'bank':self.name,
                'Date':date_string,
                'CurrencyCode':rate[0],
                'Buying':rate[1],
                'Selling':rate[2],

                })

        display_data(self.data)

           


class TsehaySpider(scrapy.Spider):
    name = "Tsehay"
    allowed_domains = ["tsehaybank.com.et"]
    start_urls = ["https://tsehaybank.com.et/exchange-rate/"]

    def __init__(self):
        self.data = []         

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()
        symbols = response.css('table tbody tr td span b::text').getall()
        
        Rates = []
        for sym in symbols:
            temp = [sym]
            counter = 0
            for price in data[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 4:
                    break
            Rates.append(temp)    

        for rate in Rates:
            self.data.append({ 
                'bank':self.name,
                'Date':response.css('div.elementor-widget-container h3.elementor-heading-title::text').get()[21:],
                'CurrencyCode':rate[0],
                'CashBuying': rate[1],
                'CashSelling':rate[2],
                'TransactionalBuying':rate[3],
                'TransactionalSelling':rate[4],           
            
                })

        display_data(self.data)

            


class WegagenSpider(scrapy.Spider):
    name = "Wegagen"
    allowed_domains = ["www.wegagen.com"]
    start_urls = ["https://www.wegagen.com/exchange-rate-cash-notes/"]

    def __init__(self):
        self.data = []           

    def parse(self, response):
        
        data = response.css('table tbody tr td::text').getall()
        data = data[2:]

        Rates = []
        temp = []
        for rate in data:
            temp.append(rate)
            if len(temp) == 6:
                Rates.append(temp)
                temp = []


        for rate in Rates:
            self.data.append({ 
                'bank':'Wegagen',
                "Date":response.css('table tbody tr td h6 strong::text').get(),
                "CurrencyCode":rate[0],
                "CashBuying":rate[2],
                "CashSelling":rate[3],
                "TransactionalBuying":rate[4],
                "TransactionalSelling":rate[5],
                })

        display_data(self.data)

           
    

class ZemenSpider(scrapy.Spider):
    name = "Zemen"
    allowed_domains = ["zemenbank.com"]
    start_urls = ["https://zemenbank.com/exchange-rates"]

    def __init__(self):
        self.data = []          

    def parse(self, response):
        
        symbol = response.css('table tbody tr.currency-entry td.currency-identity div.media div.media-body h4::text').getall()
        prices = response.css('table tbody tr.currency-entry td h5::text').getall()

        Rates = []
        for sym in symbol:
            temp = [sym]
            counter = 0
            for price in prices[len(Rates) * 2:]:
                temp.append(price)
                counter += 1
                if counter == 2:
                    break
            Rates.append(temp)

        for rate in Rates:
            self.data.append({ 
                'bank':self.name,
                "Date":response.css('table thead tr th span.text-uppercase::text').get(),
                "CurrencyCode":rate[0],
                "Buying":rate[1],
                "Selling":rate[2],
                })

        display_data(self.data)

          

def run_spider(spider_class):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })
    process.crawl(spider_class)
    process.start()
    process.stop()

if __name__ == '__main__':
    My_spiders = [AhaduSpider, AbaySpider, AmharaSpider, AwashSpider, AddisSpider,
                  BerhanSpider, BoaSpider, BunnaSpider,
                  CbeSpider, CoopSpider,
                  DashenSpider, DebubGlobalSpider,
                  EnatSpider, GadaaSpider, GohBetochSpider,
                  HibretSpider, HijraSpider, NbeSpider, NibSpider,
                  OromiaSpider, SiinqeeSpider, TsedeySpider, TsehaySpider, 
                  WegagenSpider, ZemenSpider]
    threads = []

    for spider in My_spiders:
        t = threading.Thread(target=run_spider, args=(spider,))
        add_script_run_ctx(t)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()