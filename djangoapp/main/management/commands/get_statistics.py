import pandas as pd

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

def get_vacancies(param=None):
    dtype = {
        'name': 'str',
        'salary': 'float64',
        'key_skills': 'str',
        'area_name': 'str',
        'published_at': 'str'
    }

    vacancies = pd.read_csv('filtered_vacancies', dtype=dtype)
    vacancies['salary'] = vacancies['salary'].fillna(0)
    vacancies = vacancies[vacancies['salary'] <= 10 ** 7] if param else vacancies
    vacancies.loc[:, 'published_at'] = pd.to_datetime(vacancies['published_at'], utc=True).dt.year
    return vacancies

salary_vacancies = get_vacancies('salary')
all_vacancies = get_vacancies()