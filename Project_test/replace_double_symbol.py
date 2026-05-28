# Пользователь с клавиатуры (через функцию input()) вводит строку, состоящую из символов латинского алфавита.
# Необходимо последовательно заменять две одинаковые буквы во введённой строке на следующую по алфавиту букву 
# (важно: заменяем по 2 одинаковых буквы за одну итерацию, не более). Операция замены должна повторяться до тех пор, 
# пока в строке не останутся только уникальные символы.
# Несколько важных моментов:
# буквы не обязаны быть смежными (смежные — стоящие рядом; в строке 'abc' буквы a и b, а также b и c являются смежными, 
# в то время как a и c — нет);
# zz заменяем на a;
# вводимая строка состоит из букв латинского алфавита в нижнем регистре.
# Напишите функцию replace_duplicates(), которая принимает на вход произвольную строку s, значение которой вводится 
# с клавиатуры. Функция должна последовательно производить описанную операцию и возвращать строку с оставшимися буквами 
# в любом порядке.

import string
alphabet = list(string.ascii_lowercase)
s = 'hhakafh'

def replace_duplicates(p_str):
    res_str = ''
    def get_next(p_symb):
        #Определение следующего символа
        if p_symb =='z':
            return 'a'
        
        for indx, val in enumerate(alphabet):
            if val == p_symb:
                return alphabet[indx+1]

    def get_wsymb(p_str):
        lst_str = list(p_str)
        sps_dist = set(lst_str)
        res_w = []
        
        for elem in sps_dist:
            cnt = lst_str.count(elem)
            if cnt > 1:
                res_w.append(elem)
    
        return res_w
        
    sps_w = get_wsymb(p_str)
    
    if len(sps_w) == 0:
        res_str = p_str
        return res_str
    
    for elem in sps_w:
        w_symb = elem        #дублирующийся символ
        next_symb = get_next(elem) #следующий символ для замены 
        res_str = p_str.replace(w_symb,next_symb,2) #заменить дублирующиеся символы на следующийе по алфавиту
        res_str = res_str.replace(next_symb,'',1) #удалить 1 из вставленных новых символов
    
    res_str = replace_duplicates(res_str)
    return res_str

print(replace_duplicates(s))  

