import numpy as np

def predict_number_v1(number:int=1) -> int:
    """Рандомно угадываем число
    
    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    count_predict = 0
    
    while True:
        count_predict += 1
        predict_number = np.random.randint(1,101) # Предполагаемое число
        if number == predict_number:
            break #выход из цикла, если угадали
    
    return count_predict

def predict_number_v2(number: int = 1) -> int:
    """Сначала устанавливаем любое random число, а потом уменьшаем
    или увеличиваем его в зависимости от того, больше оно или меньше нужного.
       Функция принимает загаданное число и возвращает число попыток

    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    count_predict = 0
    predict = np.random.randint(1, 101)

    while number != predict:
        count_predict += 1
        if number > predict:
            predict += 1
        elif number < predict:
            predict -= 1

    return count_predict

def predict_number_v3(number: int = 1) -> int:
    """ Сначала устанавливаем случайное число в начальном диапазоне,
        после этого используем это число для сокращения диапазона поиска 
        смещением границ: 
        если число меньше загаданног, то текущее число становится максимумом поискового диапазона
        если число больше загаданного, то - минимумом 
    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    # Ваш код начинается здесь
    count_predict = 0 
    
    #Начальный диапазон поиска
    l_start = 1
    l_end = 101
    
    predict = np.random.randint(l_start, l_end)
    
    while number != predict:
        count_predict += 1
        if number > predict:
            l_start = predict #сужаем диапазон поиска со стороны минимума
            predict  = np.random.randint(l_start,l_end)
        elif number < predict:
            l_end = predict #сужаем диапазон поиска со стороны максимума
            predict = np.random.randint(l_start,l_end)
            
    return count_predict    
    # Ваш код заканчивается здесь
    
def score_game(random_predict) -> int:
    """ Оценка алгоритма угадывания числа
        Оценивается по среднему количеству попыток из 1000 подходов
    Args:
        random_predict ([type]): Используемая функция угадывания. Defaults to 1.

    Returns:
        int: среднее количество попыток
    """
    count_predict = [] # Количество предсказаний
    np.random.seed(1) # фиксируем сид для воспроизводимости
    
    random_array = np.random.randint(1,100,size=1000) #загадали список чисел
    
    for number in random_array:
        count_predict.append(random_predict(number))
    
    score = int(np.mean(count_predict)) # находим среднее количество попыток
    
    print(f'Ваш алгоритм "{random_predict.__name__}" угадывает число в среднем за {score} попыток')
    return(score)

if __name__ == '__main__':
    score_game(predict_number_v1)
    score_game(predict_number_v2)
    score_game(predict_number_v3)
    