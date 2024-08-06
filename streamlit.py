import streamlit as st
import plotly.express as px

import pandas as pd
import mysql.connector



class Banks:
    def __init__(self):
 
        # For transactions and cash rate
        self.conn = mysql.connector.connect(
            host = st.secrets['Host'],
            user=st.secrets['Database_user'],
            password= st.secrets['Database_password'],
            database=st.secrets['Database_name'],
            port=st.secrets['Port_number']
        )
 
        self.cur = self.conn.cursor()

    # The two functions below retrieve the name of the banks
    def banks_name(self):
        self.cur.execute('select distinct bank from rates')
        banks = self.cur.fetchall()
        banks = [bank[0] for bank in banks]

        return  banks
    
    def banks_name_full(self):
        self.cur.execute('select distinct bank from full_rates')
        banks = self.cur.fetchall()
        banks = [bank[0] for bank in banks]   

        return banks      

    # This function return the date, CurrencyCode, Buying and selling rates from database for respective bank
    def rate(self, bank: str) -> str:
        
        self.cur.execute('SELECT * FROM rates WHERE bank = %s ORDER BY date DESC', (bank,))
        result = self.cur.fetchall()
        most_recent_date = result[0][1]
        recent_rates = [rate for rate in result if rate[1] == most_recent_date]

        return recent_rates
    
    # This function return the date, CurrencyCode, Cash Buying and cash selling, Transactional buying, Transactional selling rates from database for respective bank
    def full_rate(self, bank: str) -> str:
        
        self.cur.execute('SELECT * FROM full_rates WHERE bank = %s ORDER BY date DESC', (bank,))
        result = self.cur.fetchall()
        most_recent_date = result[0][1]
        recent_rates = [rate for rate in result if rate[1] == most_recent_date]

        return recent_rates 
    
    # The two functions below return the dataframe and date that is retieved from the database using the functions: full_rate() and rate()
    def bank_rate_table(self, bank: str):
        rates = self.rate(bank)
        data = [[rate[2], rate[3], rate[4]] for rate in rates if rate[3] is not None]

        return rates[0][1].strftime('%d-%m-%Y'), pd.DataFrame(data= data, columns = ['Currency code', 'Buying', 'Selling']).set_index('Currency code')
    
    def bank_full_rate_table(self, bank: str):
        rates = self.full_rate(bank)
        data = [[rate[2], rate[3], rate[4], rate[5], rate[6]] for rate in rates if rate[3] is not None]

        return rates[0][1].strftime('%d-%m-%Y'), pd.DataFrame(data= data, columns = ['Currency code', 'Cash Buying', 'Cash Selling', 'Transaction Buying', 'Transaction Selling']).set_index('Currency code')
    

    def best_rates(self):
        # Best USD rates
        self.cur.execute('select * from full_rates where CurrencyCode = %s order by TransactionalBuying DESC limit 1;', ('USD',))
        result_full = self.cur.fetchall()[0]

        self.cur.execute('select * from rates where CurrencyCode = %s order by Buying DESC limit 1;', ('USD',))
        result = self.cur.fetchall()[0]        

        best_rate = result[3]
        best_full_rate = result_full[5]

        best_USD = result if best_rate > best_full_rate else result_full

        # Best EUR rates
        self.cur.execute('select * from full_rates where CurrencyCode = %s order by TransactionalBuying DESC limit 1;', ('EUR',))
        result_full = self.cur.fetchall()[0]

        self.cur.execute('select * from rates where CurrencyCode = %s order by Buying DESC limit 1;', ('EUR',))
        result = self.cur.fetchall()[0]        

        best_rate = result[3]
        best_full_rate = result_full[5]

        best_EUR = result if best_rate > best_full_rate else result_full        

        # Best GBP rates
        self.cur.execute('select * from full_rates where CurrencyCode = %s order by TransactionalBuying DESC limit 1;', ('GBP',))
        result_full = self.cur.fetchall()[0]

        self.cur.execute('select * from rates where CurrencyCode = %s order by Buying DESC limit 1;', ('GBP',))
        result = self.cur.fetchall()[0]        

        best_rate = result[3]
        best_full_rate = result_full[5]

        best_GBP = result if best_rate > best_full_rate else result_full          

        best_rates = [list(best_USD), list(best_EUR), list(best_GBP)]


        for best in best_rates:
            best[1] = best[1].strftime('%d-%m-%Y')
            if len(best) == 7:
                best[3] = best[5]
                best[4] = best[6]
                best.pop()
                best.pop()

            best[0], best[1] = best[1], best[0]
            

        return  pd.DataFrame(data =best_rates, columns = ['Date', 'Bank', 'Currency Code', 'Buying', 'Selling']).set_index('Date')
    
    def visualize_historical_data(self):
        self.cur.execute('select Date, TransactionalSelling from full_rates where bank = %s AND CurrencyCode = %s order by date desc limit 30', ('CBE', 'USD'))
        data = self.cur.fetchall()

        data= [[pd.to_datetime(price[0], format='%d-%m-%Y'), float(price[1])] for price in data]

        USD_df = pd.DataFrame(data, columns=['Date', 'Currency selling']).set_index('Date')
        USD_df.index = pd.to_datetime(USD_df.index)
        USD_df.sort_index(inplace=True)

        fig = px.line(USD_df, y='Currency selling')
    
        return fig

class Ui:
    def __init__(self):
        
        st.set_page_config(layout="wide")

        st.title('Exchange Rate')
        st.header('Best Currency rates in Ethiopia')

        banks = Banks()
        banks_name = banks.banks_name()
        banks_name_full = banks.banks_name_full()

        Banks_name = banks_name + banks_name_full
        Banks_name.sort()

        st.write('These are the best currency rates in Ethiopia right now')
        st.dataframe(banks.best_rates(), width = 1000)

        st.header('Commercial Bank of Ethiopia USD selling rate')
        st.plotly_chart(banks.visualize_historical_data())
        
        st.header('List of Currency rates')
        for name in Banks_name:
            with st.expander(f'{name} bank exchange rate'):
                if name in banks_name_full:
                    date, rates = banks.bank_full_rate_table(name)
                else:
                    date, rates = banks.bank_rate_table(name)

                st.write('Last updated', date)
                st.dataframe(rates, width = 1000)



 
        


if __name__ == '__main__':
    ui = Ui()
    


            
        