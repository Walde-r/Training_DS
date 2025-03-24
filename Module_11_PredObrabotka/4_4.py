import pandas as pd

list_test = ['Опыт работы 8 лет 3 месяца',
             'Опыт работы 3 года 5 месяцев',
             'Опыт работы 1 год 9 месяцев',
             'Опыт работы 3 месяца',
             'Опыт работы 6 лет']

test_df = pd.DataFrame(list_test, columns=['Stag_Job'])



def get_experience(arg):
    """аргумент: которой является строка столбца с опытом работы. 
    Функция должна возвращать опыт работы в месяцах. 
    Не забудьте привести результат к целому числу.
    Примечание. Обратите внимание, что опыт работы может выражаться только в годах или только в месяцах. 
    Учтите это при построении своей функции."""
    res_month = 0
    
    l_words = arg.split(' ')

    if len(l_words) == 6:
        res_month = int(l_words[2]) * 12 + int(l_words[4])
    else:
        if str(l_words[3]).find('месяц') != -1:
            res_month = int(l_words[2])
        else:
            res_month = int(l_words[2]) * 12       
    
    return res_month

print(test_df['Stag_Job'].apply(get_experience))

