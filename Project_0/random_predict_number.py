import numpy as pn

def random_predict(number:int=1) -> int:
    """Рандомно угадываем число

    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    count = 0
    
    while True:
        count += 1
        predict_number = pn.random.randint(1,101) # Предполагаемое число
        if number == predict_number:
            break #выход из цикла, если угадали
    
    return count

def score_game(number:int=1) -> int:
    """За какое количество попыток в среднем из 1000 подходов угадывает наш алгоритм

    Args:
        random_predict ([type]): функция угадывания. Defaults to 1.

    Returns:
        int: среднее количество попыток
    """
    count_ls = []
    pn.random.seed(1) # фиксируем сид для воспроизводимости
    random_array = pn.random.randint(1,100,size=1000) #загадали список чисел
    
    for number in random_array:
        count_ls.append(random_predict(number))
    
    score = int(pn.mean(count_ls)) # находим среднее количество попыток
    print(f'Ваш алгоритм угадывает число в среднем за {score} попыток')
    return(score)

if __name__ == '__main__':
    score_game(random_predict)
    