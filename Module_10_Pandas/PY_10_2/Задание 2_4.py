import pandas as pd

names = ['chlorhexidine', 'cyntomycin', 'afobazol'] 
counts = [15, 18, 7]

def create_medications(names, counts):
    """ Функция создает Series medications, 
    ндексами которой являются названия лекарств names, 
    а значениями - их количество в поставке counts"""
    
    medications = pd.Series(data= counts, index=names)
    return medications

def get_percent(medications, name):
    """возвращает долю количества товара с именем name 
    от общего количества товаров в поставке в процентах"""

    return medications[name]/medications.sum()*100


print(get_percent(create_medications(names, counts),'chlorhexidine'))