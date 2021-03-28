import credentials
from datetime import datetime as dt
from datetime import timedelta as td
import pandas as pd 
from binance.client import Client

# CREATE CLIENT OBJECT AND TEST THE CONNECTION
client = Client(credentials.API_KEY, credentials.API_SECRET)
try:
    time_res = client.get_server_time()
except BinanceAPIException as e:
    print (e.status_code)
    print (e.message)

# FUNCTION TO GET ONE MINUTE KLINE FROM TIMESTAMP
def getMinute(in_timestamp):
    #print('IN_TIMESTAMP =', in_timestamp)
    date = dt.fromtimestamp(in_timestamp)
    init_date = date - td(seconds=date.second)
    add_minute = td(minutes=1)
    final_date = init_date + add_minute

    return init_date.strftime("%m/%d/%Y, %H:%M:%S"), final_date.strftime("%m/%d/%Y, %H:%M:%S")


# ITERATE DATAFRAME TO OBTAIN THE OUTPUT PRICE
df = pd.read_csv('trades.csv')
df.sort_index(inplace=True, ascending=False, ignore_index=True)

#input_timestamp = 1610816143
fiats =         ['USDT', 'BUSD', 'USDC']
fiats_pairs =   ['EURUSDT', 'EURBUSD', 'EURUSDC']

list_eur_prices = []
for index, row in df.iterrows():
    if row['Output'] in fiats:
        index_fiat = fiats.index(row['Output'])
        f, s = getMinute(row['Date(UTC)'])
        #print('INIT MINUTE =', f)
        #print('FINAL MINUTE =', s)
        klines = client.get_historical_klines(fiats_pairs[index_fiat], Client.KLINE_INTERVAL_1MINUTE, f, s)
        price = list_eur_prices.append(klines[0][4])
        print('CLOSE PRICE OF', fiats_pairs[index_fiat], '=', klines[0][4], 'AT', s)
    elif row['Output'] == 'EUR':
        price = list_eur_prices.append(1)
    else:
        print('ERROR FIAT NOT FOUND')
    
df['EUR Price'] = list_eur_prices

df.to_csv('trades_w_eur.csv', encoding='utf-8', index=False)