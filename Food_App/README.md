# Исследование мобильного приложения по продаже продуктов

[Исследование в HTML](https://alexslobodskoj.github.io/Portfolio/Food_App/food_app.html)

[Исследование в Jupiter Notebook](https://github.com/AlexSlobodskoj/Portfolio/blob/main/Food_App/food_app.ipynb)

## Цели исследования

- изучить воронку продаж
- исследовать результаты A/A/B-эксперимента по замене шрифта во всем приложении

## Навыки и инструменты

- **python**
- **pandas**
- **matplotlib**
- **seaborn**
- **numpy**
- scipy.stats.**ttest_ind**
- scipy.stats.**mannwhitneyu**
- statsmodels.stats.proportion.**proportions_ztest**
- plotly.**graph_objects**
- выбор статистического критерия

## Результаты

- установлен этап воронки продаж с максимальной долей (**38%**) потери пользователей
- различия в конверсии экспериментальной группы пользователей, использовавших приложение с новыми шрифтами, не являются статистически значимыми
- рекомендовано  оставить исходный шрифт
