from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="index"),
    path('statisctics/', views.get_statistics, name='statistics'),
    path('demand/', views.get_demand, name='demand'),
    path('geography/', views.get_geography, name='geography'),
    path('skills/', views.get_skills, name='skills'),
    path('last_vacancies/', views.get_last_vacancies, name='last_vacancies'),
]
