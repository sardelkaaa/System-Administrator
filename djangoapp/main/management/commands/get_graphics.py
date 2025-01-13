import numpy as np
from django.core.management.base import BaseCommand
import pandas as pd
from main.models import Vacancy
from matplotlib import pyplot as plt
from collections import Counter


class Command(BaseCommand):
    help = 'Получение графиков в static'

    def handle(self, *args, **kwargs):
        def get_dynamic_by_years(vacancies, dynamic_for):
            result = vacancies.groupby('published_at').agg({
                dynamic_for: 'mean' if dynamic_for == 'salary' else 'count'
            }).round().astype(int).reset_index().sort_values(by='published_at')

            return result.sort_values('published_at').set_index('published_at')[dynamic_for]

        def get_dynamic_by_cities(vacancies, dynamic_for):
            result = vacancies.groupby(['area_name']).agg({
                dynamic_for: 'mean' if dynamic_for == 'salary' else 'count'
            }).round().astype(int).reset_index().sort_values(by=[dynamic_for, 'area_name'], ascending=[False, True])

            result[dynamic_for] = (((result[dynamic_for] / len(vacancies) * 100)
                                    .astype(float)).round(2)) if dynamic_for != 'salary' else result[dynamic_for]
            return result.set_index('area_name')[dynamic_for]

        def get_statistics_by_years(vacancies, param, vac_name=None):
            if vac_name:
                vacancies = vacancies[vacancies['name'].str.contains(vac_name, regex=False, case=False, na=False)]

            if param == 'salary':
                return get_dynamic_by_years(vacancies, 'salary').to_dict()
            return get_dynamic_by_years(vacancies, 'name').to_dict()

        def get_statistics_by_cities(vacancies, param):
            stats_count_by_cities = get_dynamic_by_cities(vacancies, 'name')
            stats_count_by_cities = stats_count_by_cities[stats_count_by_cities > 1]

            if param == 'salary':
                stats_salary_by_cities = get_dynamic_by_cities(vacancies, 'salary')
                stats_salary_by_cities = stats_salary_by_cities[
                    stats_salary_by_cities.index.isin(stats_count_by_cities.index)].head(20).to_dict()
                return stats_salary_by_cities
            return stats_count_by_cities.to_dict()

        def get_top_skills(vacancies):
            vacancies = vacancies[vacancies['key_skills'] != 'nan']
            vacancies['key_skills'] = vacancies['key_skills'].str.split('\n')
            vacancies = vacancies.groupby(['published_at'])['key_skills'].apply(list)

            most_popular_skills = {}
            for year, skills_lists in vacancies.items():
                all_skills = [skill for skills in skills_lists for skill in skills]
                if all_skills:
                    skills_count = Counter(all_skills)
                    most_common_skill = skills_count.most_common(2)
                    most_popular_skills[year] = {
                        'skill': [most_common_skill[i][0] for i in range(2)],
                        'count': [most_common_skill[i][1] for i in range(2)]
                    }
            return most_popular_skills

        def get_vacancies(param=None):
            vacancies = pd.DataFrame.from_records(Vacancy.objects.values().all())
            vacancies['salary'] = vacancies['salary'].fillna(0)
            vacancies = vacancies[vacancies['salary'] <= 10 ** 7] if param else vacancies
            vacancies.loc[:, 'published_at'] = pd.to_datetime(vacancies['published_at'], utc=True).dt.year
            return vacancies

        salary_vacancies = get_vacancies('salary')
        all_vacancies = get_vacancies()

        def get_graph_and_table(x, y, title, graph_color, table_color, graph_name, table_name, x_name, y_name, segment):
            plt.figure(figsize=(10, 8))
            plt.plot(x, y, marker='o', color=graph_color)
            plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
            plt.tick_params(axis='x', rotation=90)
            plt.yticks(np.arange(0.0, max(y), segment))
            plt.title(title)
            plt.grid(True, linestyle='--')
            plt.savefig(f'main/static/graphics_and_tables/{graph_name}')

            fig, ax = plt.subplots(figsize=(6, 8))
            table_data = pd.DataFrame({x_name: x, y_name: y})
            table = ax.table(cellText=table_data.values,
                             colLabels=table_data.columns,
                             loc='center',
                             cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)

            for k, cell in table.get_celld().items():
                if k[0] == 0:
                    cell.set_facecolor(table_color)

            ax.axis('off')
            fig.tight_layout()
            plt.savefig(f'main/static/graphics_and_tables/{table_name}')
            plt.close(fig)
            plt.close()

        def get_barh_and_table(x, y, title, histogram_color, table_color, histogram_name, table_name, x_name,
                                    y_name):
            plt.figure(figsize=(10, 8))
            plt.barh(y, x, color=histogram_color)
            plt.xticks(np.arange(0.0, max(x) + 1, 5000.0))
            plt.tick_params(axis='x', rotation=90)
            plt.title(title)
            plt.grid(True, linestyle='--')
            plt.savefig(f'main/static/graphics_and_tables/{histogram_name}')

            fig, ax = plt.subplots(figsize=(6, 8))
            table_data = pd.DataFrame({x_name: y, y_name: x})
            table = ax.table(cellText=table_data.values,
                             colLabels=table_data.columns,
                             loc='center',
                             cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)

            for k, cell in table.get_celld().items():
                if k[0] == 0:
                    cell.set_facecolor(table_color)

            ax.axis('off')
            fig.tight_layout()
            plt.savefig(f'main/static/graphics_and_tables/{table_name}')
            plt.close(fig)
            plt.close()

        def get_pie_and_table(x, y, y_table, title, table_color, pie_name, table_name, x_name, y_name):
            values = y[:20]
            labels = x[:20]
            plt.figure(figsize=(10, 8))
            plt.title(title)
            plt.pie(values, labels=labels, textprops={'fontsize': '6'})
            plt.savefig(f'main/static/graphics_and_tables/{pie_name}')
            fig, ax = plt.subplots(figsize=(6, 8))
            table_data = pd.DataFrame({x_name: x, y_name: y_table})
            table = ax.table(cellText=table_data.values,
                             colLabels=table_data.columns,
                             loc='center',
                             cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)

            for k, cell in table.get_celld().items():
                if k[0] == 0:
                    cell.set_facecolor(table_color)

            ax.axis('off')
            fig.tight_layout()
            plt.savefig(f'main/static/graphics_and_tables/{table_name}')
            plt.close(fig)
            plt.close()


        # Первый график
        salary_by_years = get_statistics_by_years(salary_vacancies, 'salary')
        salary_years = list(salary_by_years.keys())
        salaries_by_year = list(salary_by_years.values())
        get_graph_and_table(
            salary_years, salaries_by_year,
            'Динамика уровня зарплат по годам',
            'gold', '#FFCF48',
            'salary_by_years_graph.png',
            'salary_by_years_table.png',
            'Год', 'Средняя з/п',
            5000.0
        )

        # Второй график
        count_by_years = get_statistics_by_years(all_vacancies, 'count')
        count_years = list(count_by_years.keys())
        counts_by_years = list(count_by_years.values())
        get_graph_and_table(
            count_years, counts_by_years,
            'Динамика количества вакансий по годам',
            'blue', '#1240AB',
            'count_by_years_graph.png',
            'count_by_years_table.png',
            'Год', 'Количество вакансий',
            50000.0
        )

        # Третий график
        salary_by_cities = get_statistics_by_cities(salary_vacancies, 'salary')
        salary_cities = list(salary_by_cities.keys())
        salaries_by_cities = list(salary_by_cities.values())
        get_barh_and_table(
            salaries_by_cities, salary_cities,
            'Уровень зарплат по городам',
            'darkred', '#5E2129',
            'salary_by_cities_graph.png',
            'salary_by_cities_table.png',
            'Город', 'Средняя з/п'
        )

        # Четвёртый график
        share_by_cities = get_statistics_by_cities(all_vacancies, 'count')
        share_cities = list(share_by_cities.keys())
        shares_by_cities = list(share_by_cities.values())
        get_pie_and_table(
            share_cities, shares_by_cities, shares_by_cities,
            'Доля вакансий по городам', 'green',
            'share_by_cities_graph.png',
            'share_by_cities_table.png',
            'Город', 'Доля вакансий'
        )

        # Пятый график

        skills_by_years = get_top_skills(all_vacancies)
        years = list(skills_by_years.keys())
        counts = []
        skills = []
        for year in years:
            counts.append(sum(skills_by_years[year]['count']))
            skills.append(skills_by_years[year]['skill'])

        print(years, counts, skills)

        get_pie_and_table(
            years, counts, skills,
            'ТОП-20 навыков по годам', 'purple',
            'top_skills_graph.png',
            'top_skills_table.png',
            'Год', 'Навыки'
        )

        self.stdout.write(self.style.SUCCESS('Графики созданы успешно!'))