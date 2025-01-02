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
    return render(request, 'main/last_vacancies.html')