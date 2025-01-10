from django.db import models

class Currency(models.Model):
    date = models.DateField()
    BYR = models.FloatField(null=True, blank=True)
    USD = models.FloatField(null=True, blank=True)
    EUR = models.FloatField(null=True, blank=True)
    KZT = models.FloatField(null=True, blank=True)
    UAH = models.FloatField(null=True, blank=True)
    AZN = models.FloatField(null=True, blank=True)
    KGS = models.FloatField(null=True, blank=True)
    UZS = models.FloatField(null=True, blank=True)
    GEL = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'main_currencyrate'

    def __str__(self):
        return f"{self.date} rates"

class Vacancy(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    key_skills = models.TextField(null=True, blank=True)
    salary_from = models.FloatField(null=True, blank=True)
    salary_to = models.FloatField(null=True, blank=True)
    salary_currency = models.CharField(max_length=10, null=True, blank=True)
    area_name = models.CharField(max_length=255, null=True, blank=True)
    published_at = models.DateField(null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name