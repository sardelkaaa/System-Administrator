import pandas as pd


'''Перевод зарплат в рубли'''

url = 'http://www.cbr.ru/scripts/XML_daily.asp'
currencies = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']
date = pd.to_datetime('2003-01-01')
end_date = pd.to_datetime('2025-01-01')
currency = []

while end_date >= date:
    date_req = f'?date_req={date.strftime("%d/%m/%Y")}'
    curr_url = url + date_req
    df = pd.read_xml(curr_url, xpath='.//Valute', encoding="ISO-8859-1")
    df['VunitRate'] = df['VunitRate'].str.replace(',', '.').astype(float)
    df['VunitRate'] = round(df['VunitRate'], 8)

    df = df.loc[df['CharCode'].isin(currencies), ['CharCode', 'VunitRate']].set_index('CharCode').T
    df.insert(0, 'date', date.strftime('%Y-%m'))
    currency.append(df.to_dict(orient='records')[0])

    date += pd.DateOffset(months=1)

currency = pd.DataFrame(currency)
currency.to_csv('currency.csv', index=False)