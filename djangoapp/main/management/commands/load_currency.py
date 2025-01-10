from django.core.management.base import BaseCommand
import pandas as pd
from main.models import Currency


class Command(BaseCommand):
    help = 'Загрузка курсов валют в базу данных'

    def handle(self, *args, **kwargs):

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
            df.insert(0, 'date', date)
            currency.append(df.to_dict(orient='records')[0])

            date += pd.DateOffset(months=1)

        currency_df = pd.DataFrame(currency)
        currency_df.reset_index()
        for _, row in currency_df.iterrows():
            Currency.objects.create(
                date=row.get('date'),
                BYR=row.get('BYR'),
                USD=row.get('USD'),
                EUR=row.get('EUR'),
                KZT=row.get('KZT'),
                UAH=row.get('UAH'),
                AZN=row.get('AZN'),
                KGS=row.get('KGS'),
                UZS=row.get('UZS'),
                GEL=row.get('GEL'),
            )

        self.stdout.write(self.style.SUCCESS('Курсы валют успешно загружены!'))