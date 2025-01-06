import matplotlib.pyplot as plt
import numpy as np
from get_statistics import *


salary_by_years = get_statistics_by_years(filtered_vacancies, 'salary')
years = list(salary_by_years.keys())
salaries = list(salary_by_years.values())

plt.figure(figsize=(10, 8))
plt.plot(years, salaries, marker='o', color='gold')
plt.xticks(np.arange(min(years), max(years) + 1, 1.0))
plt.tick_params(axis='x', rotation=90)
plt.yticks(np.arange(0.0, 50000.0, 5000.0))
plt.title('Динамика уровня зарплат по годам')
plt.grid(True, linestyle='--')
plt.savefig('../static/graphics_and_tables/salary_by_years_graph.png')


fig, ax = plt.subplots(figsize=(6, 8))
table_data = pd.DataFrame({'Год': years, 'Средняя Зарплата': salaries})
table = ax.table(cellText=table_data.values,
                  colLabels=table_data.columns,
                  loc='center',
                  cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)

for k, cell in table.get_celld().items():
    if k[0] == 0:
        cell.set_facecolor('#FFCF48')

ax.axis('off')
fig.tight_layout()
plt.savefig('../static/graphics_and_tables/salary_by_years_table.png')
plt.close(fig)
plt.close()