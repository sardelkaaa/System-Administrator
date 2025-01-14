from datetime import datetime, timedelta
import requests
from django.shortcuts import render


def home(request):
    return render(request, 'main/index.html')

def get_statistics(request):
    return render(request, 'main/statistics.html')

def get_demand(request):
    return render(request, 'main/demand.html')

def get_geography(request):
    return render(request, 'main/geography.html')

def get_skills(request):
    return render(request, 'main/skills.html')

def get_last_vacancies(request):
    now = datetime.now()

    time = now - timedelta(hours=24)

    str_time = time.strftime('%Y-%m-%dT%H:%M:%S')

    response = requests.get('https://api.hh.ru/vacancies', params={
        'text': 'System Administrator',
        'date_from': str_time,
        'per_page': 10,
        'order_by': 'publication_time'
    })


    vacancies = response.json()['items']

    for vacancy in vacancies:
        vacancy_id = vacancy['id']
        vacancy_response = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
        key_skills = vacancy_response.json().get('key_skills', [])
        vacancy['key_skills'] = ', '.join([skill['name'] for skill in key_skills])
        description = vacancy_response.json().get('description')
        vacancy['description'] = description

    return render(request, 'main/last_vacancies.html', {'vacancies': vacancies})