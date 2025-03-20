import numpy as np

def get_chess(a):
    """принимает на вход длину стороны квадрата a и возвращает двумерный массив формы (a, a), 
       заполненный 0 и 1 в шахматном порядке. В левом верхнем углу всегда должен быть ноль: 
       my_collection[start:stop:step]  # старт, стоп и шаг

    Args:
        a (_type_): np.ndarray
    """
    
    res_arr = np.zeros((a,a))
    
    res_arr[::2,1::2] = 1 # нумеруется каждый второй слобец, для каждой второй строки начисна я с первой
    res_arr[1::2,::2] = 1  # нумеруется каждая вторая строка начиная со второй (0,1), для каждого второго столбца
    
    
   
    return res_arr
    
def shuffle_seed(array):
    """принимает на вход массив из чисел, 
    генерирует случайное число для seed в диапазоне от 0 до 2**32 - 1 (включительно) 
    и возвращает кортеж: перемешанный с данным seed массив (исходный массив должен оставаться без изменений), 
    а также seed, с которым этот массив был получен

    Args:
        array (_type_): typle
    """
    res_arr = np.array(array)
    l_seed = np.random.randint(0,2**32-1,dtype=np.uint32)
    np.random.seed(l_seed)
    np.random.shuffle(res_arr)
    
    return (res_arr, int(l_seed))
    
def min_max_dist(*vectors):
    """функция принимает на вход неограниченное число векторов через запятую. 
    Гарантируется, что все векторы, которые передаются, одинаковой длины.
    Функция возвращает минимальное и максимальное расстояние между векторами в виде кортежа."""
    min_len = 0
    max_len  = 0
    
    cur_len = np.linalg.norm(vectors[0]-vectors[len(vectors)-1]) 
    min_len = cur_len
    max_len = cur_len
    
    
    for i in range(len(vectors)-2):
        cur_len = np.linalg.norm(vectors[i]-vectors[i+1])
        
        if cur_len > max_len:
            max_len = cur_len
        else:
            if cur_len < min_len:
                min_len = cur_len        
        
    
    return (float(min_len), float(max_len))

def any_normal(*vectors):
    """принимает на вход неограниченное число векторов через запятую. 
    Гарантируется, что все векторы, которые передаются, одинаковой длины.
    Функция возвращает True, если есть хотя бы одна пара перпендикулярных векторов np.dot(v1,v2) == 0. 
    Иначе возвращает False.
    """
    res_normal = False
    
    l_dot = np.dot(vectors[0],vectors[len(vectors)-1])
    
    if l_dot == 0:
        res_normal = True
    else:
        for i in range(len(vectors)-1):
            l_dot = np.dot(vectors[i],vectors[i+1])
            if l_dot == 0:
                res_normal = True
                break

    return res_normal         

def get_loto(num):
    """функция генерирует трёхмерный массив случайных целых чисел от 1 до 100 (включительно). 
    Это поля для игры в лото.
    Трёхмерный массив должен состоять из таблиц чисел формы 5х5, то есть итоговая форма — (num, 5, 5).
    
    Args:
        num (_type_): Функция возвращает полученный массив
    """
    
    res_arr = np.random.randint(1, 101, size=(num,5,5), dtype = np.uint8)

    return(res_arr)

def get_unique_loto(num):
    """функция генерирует трёхмерный массив случайных УНИКАЛЬНЫХ целых чисел от 1 до 100 (включительно). 
    Это поля для игры в лото.
    Трёхмерный массив должен состоять из таблиц чисел формы 5х5, то есть итоговая форма — (num, 5, 5).
    
    Args:
        num (_type_): Функция возвращает полученный массив
    """
    i = 1
    res_arr  = np.random.choice(101, (5,5), replace=False)
    
    for i in range(num-1):
        
        next_arr = np.random.choice(101, (5,5), replace=False)
        res_arr = np.vstack([res_arr, next_arr])
     
    res_arr = res_arr.reshape(num,5,5)
   
    return(res_arr)


simplelist = [19, 242, 14, 152, 142, 1000]

print(np.mean(simplelist))