import pandas as pd
import datetime

# IMPORTAR EL CSV DE BINANCE Y CREAR EL DATAFRAME DE PANDAS
df = pd.read_csv('report.csv')
df.sort_index(inplace=True, ascending=False, ignore_index=True)
#print(df)

"""
# FUNCION DE EXTRAER UN SUBSTRING EN PYTHON
def f_substring(s, start, end):
    idx_start = s.index(start) #obtenemos la posición del carácter c
    idx_end = s.index(end) #obtenemos la posición del carácter h
    return s[idx_start:idx_end]
"""

# A PARTIR DE UNA LISTA DE BASECOINS, EXTRAER LOS 2 ELEMENTOS DE LA PERMUTA
def getPair(pairs_list):
    fiats = ['EUR', 'USDT', 'BUSD', 'USDC']
    inputs = []
    outputs = []
    for pair in pairs_list: # EXAMINAR CADA PERMUTA
        for fiat in fiats: # BUSCAR SI UTILIZA UNA STABLECOIN DE LA LISTA Y CORTAR EL STRING
            pos = pair.find(fiat)
            if pos > 0:
                # Cut the pair
                l, r = pair[:pos], pair[pos:]
                inputs.append(l)
                outputs.append(r)
                #print('L:', l)
                #print('R:', r)
                break
            #else:
                #print('CANNOT SPLIT', pair, 'WITH', fiat)
    return inputs, outputs

# OBTENER LAS LISTAS DE BASECOINS Y ASSETS
ins, outs = getPair(df['Pair'])
#print('INPUTS', ins)
#print('OUTPUTS', outs)

# AÑADIR LAS DOS LISTAS AL DATAFRAME
df['Input'] = ins
df['Output'] = outs
#print(df)

# ELIMINAR BASE EN LA COLUMNA Amount Y CONVERTIR A float
def amount_to_float(amount, fiat):
    #print('AMOUNT:', amount)
    #print('FIAT:', fiat)
    s = amount.replace(fiat, '')
    s = s.replace('BNB', '') # SI PAGAMOS LAS FEE CON BNB
    try:
        return float(s.replace(',', '')) # ELIMINAR LA COMA DE MILES
    except:
        return float(s) #0 #False

# OBTENER EL TIMESTAMP UTC
def get_timestamp(date):
    any = int(date[:4])
    mes = int(date[5:7])
    dia = int(date[8:10])
    hora = int(date[11:13])
    min = int(date[14:16])
    sec = int(date[17:19])
    date = datetime.datetime(any, mes, dia, hora, min, sec)
    return datetime.datetime.timestamp(date)

#
list_amount = []
list_exe = []
list_buy = []
list_fee = []
list_date = []
for index, row in df.iterrows():
    qnty = amount_to_float(row['Amount'], row['Output'])
    exe = amount_to_float(row['Executed'], row['Input'])
    bBuy = row['Side'] == 'BUY'
    if bBuy:
        fee = amount_to_float(row['Fee'], row['Input'])
    else:
        fee = amount_to_float(row['Fee'], row['Output'])
    date = get_timestamp(row['Date(UTC)'])
    list_amount.append(qnty)
    list_exe.append(exe)
    list_buy.append(bBuy)
    list_fee.append(fee)
    list_date.append(date)
#print(list_amount)

df['Amount'] = list_amount
df['Executed'] = list_exe
df['Side'] = list_buy
df.rename(columns={'Side': 'Buy'}, inplace=True)
df['Fee'] = list_fee
df['Date(UTC)'] = list_date
print(df)

# CREAR LA COLUMNA DE RELACION ENTRE OUTPUT Y EUR
list_eur = []
for index, row in df.iterrows():
    if row['Output'] == 'EUR':
        #print('EL OUTPUT YA ESTA EN EUR')
        list_eur.append(1)
    else: # BUSCAR PRECIO DE OUTPUT EN EUR CUANDO TIMESTAMP - BINANCE API
        print('BUSCAR EN BINANCE API')

print('list_eur:', list_eur)
print('LEN list_eur:', len(list_eur))
df['RelEUR'] = list_eur


df.to_csv('trades.csv', encoding='utf-8', index=False)

####################### la funcio fee falla

"""
for index, row in df.iterrows():
    print('ROW:', row)
    if row['Side'] == 'BUY':
        print('AUGMENTAR', row['Amount'], row['Input'], 'I DISMINUIR', row['Price']*row['Amount'], row['Output'])
    elif row['Side'] == 'SELL':
        print('AUGMENTAR', row['Output'], 'I DISMINUIR', row['Input'])
    else:
        print('ERROR')
        """