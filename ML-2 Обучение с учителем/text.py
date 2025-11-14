#Дан набор данных (50_Startups.zip) о стартапах и их прибыли (в долларах) в трёх различных штатах США.
# Столбцы:
# R&D Spend — расходы на исследования.
# Administration — административные расходы.
# Marketing Spend — расходы на маркетинг.
# State — штат.
# Profit — прибыль (целевой признак).
# Для обучения линейной регрессии используйте R&D Spend, Administration и Marketing Spend.
# Отделите факторы от целевой переменной.
# Обучите модель линейной регрессии методом наименьших квадратов
# с помощью библиотеки numpy (воспользуйтесь формулой из модуля).
# Чему равны коэффициенты линейной регрессии при признаках R&D Spend, Administration и Marketing Spend?
# Ответ введите с точностью до второго знака после точки-разделителя.

import numpy as np #для матричных вычислений
import pandas as pd #для анализа и предобработки данных
#import matplotlib.pyplot as plt #для визуализации
#import seaborn as sns #для визуализации
#from sklearn import linear_model #линейные модели
#from sklearn import metrics #метрики
#%matplotlib inline
#plt.style.use('seaborn-v0_8')


def linear_regression(X, y):
    #Создаём вектор из единиц
    ones = np.ones(X.shape[0])
    #Добавляем вектор к таблице первым столбцом
    X = np.column_stack([ones, X])
    #Вычисляем обратную матрицу Q
    Q = np.linalg.inv(X.T @ X)
    #Вычисляем вектор коэффициентов
    w = Q @ X.T @ y
    return w


startUps = pd.read_csv('ML-2 Обучение с учителем/data/50_Startups.zip', sep=',')
#startUps.info()

X = startUps[['R&D Spend', 'Administration', 'Marketing Spend']]
y = startUps['Profit']

#Вычисляем параметры линейной регрессии
w = linear_regression(X, y)

#Выводим вычисленные значения параметров
print(f'R&D Spend: {w[1].round(2)}')
print(f'Administration: {w[2].round(2)}')
print(f'Marketing Spend: {w[3].round(2)}')

#Выводим параметры с точностью до двух знаков после запятой
#print('w0: {:.2f}'.format(w[0]))
#print('w1: {:.2f}'.format(w[1]))
