
# Вам необходимо написать функцию concat_user_files(path), параметром которой является path — путь до директории.
# Функция должна:
# Объединить информацию из всех csv-файлов в единый DataFrame.
# Удалить дубликаты.
# Обновить индексы результирующей таблицы.
# Отсортировать пользователей по числовой части user_id (игнорируя буквенную часть).
# Например, если в директории users есть несколько csv-файлов, то результирующая таблица должна выглядеть так:

# Введите свое решение ниже

import os
import pandas as pd

path = './Root/users'


def concat_user_files(path):

    #список всех файлов в директории 
    all_files = os.listdir(path)
    # Фильтруем только CSV файлы
    csv_files = [file for file in all_files if file.endswith('.csv')]
    
    
    res_Data = pd.DataFrame()
    
    for use_file in csv_files:
        file_name = os.path.join(path,use_file)
        fl_data = pd.read_csv(file_name)
        
        if res_Data.shape[0] == 0:
            res_Data = fl_data.copy()
        else:
            res_Data = pd.concat([res_Data,fl_data],axis=0)
    
    res_Data['only_id'] = res_Data['user_id'].apply(lambda x: int(x[2:]))
    res_Data = res_Data.sort_values(by='only_id')
    res_Data = res_Data.drop_duplicates(ignore_index=True)
    res_Data = res_Data.drop('only_id', axis=1)
    
    return(res_Data)
    
concat_user_files(path)