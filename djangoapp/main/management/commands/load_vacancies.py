from locale import currency

import pandas as pd
from django.core.management.base import BaseCommand
from main.models import Currency, Vacancy


class Command(BaseCommand):
    help = 'Import vacancies from a CSV file'

    def handle(self, *args, **kwargs):
        def format_salary(row, df_currency):
            salary = row['salary']
            currency = row['salary_currency']
            published_at = pd.to_datetime(row['published_at']).strftime('%Y-%m')
            if pd.isna(salary):
                return salary

            if currency == 'RUR' or pd.isna(currency):
                return salary

            match_value = df_currency.loc[df_currency['date'] == published_at, currency]
            return round(salary * match_value.values[0], 2)

        def get_formatted_vacancies(csv_merged, df_currency):
            csv_merged.index += 1
            csv_merged.insert(1, 'salary', csv_merged[['salary_to', 'salary_from']].mean(axis=1).to_list())
            csv_merged['salary'] = csv_merged.apply(format_salary, axis=1, df_currency=df_currency)
            return csv_merged.drop(['salary_from', 'salary_to', 'salary_currency'], axis=1)

        currencies = pd.DataFrame.from_records(Currency.objects.values().all())
        currencies['date'] = pd.to_datetime(currencies['date']).dt.strftime('%Y-%m')

        dtype_dict = {
            'name': 'str',
            'key_skills': 'str',
            'salary_from': 'float64',
            'salary_to': 'float64',
            'salary_currency': 'str',
            'area_name': 'str',
            'published_at': 'str'
        }
        csv_merged = pd.read_csv('vacancies_2024.csv', dtype=dtype_dict)
        vacancies = get_formatted_vacancies(csv_merged, currencies)

        filtered_vacancies = [
            Vacancy(
                name=row['name'],
                key_skills=row['key_skills'],
                salary=row['salary'],
                area_name=row['area_name'],
                published_at=pd.to_datetime(row['published_at']),

            )
            for index, row in vacancies.iterrows()
        ]

        Vacancy.objects.bulk_create(filtered_vacancies, batch_size=1000)
        self.stdout.write(self.style.SUCCESS('Successfully imported vacancies'))
