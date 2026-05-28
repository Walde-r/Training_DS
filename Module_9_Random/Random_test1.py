import numpy as np
np.random.seed(2021)

simple = np.random.uniform(0,1)   #сохраните случайное число в диапазоне от 0 до 1
randoms = np.random.uniform(-150, 2021, size=120)    #Сгенерируйте 120 чисел в диапазоне от -150 до 2021
table = np.random.randint(1,101,size=(3,2)) #Получите массив из случайных целых чисел от 1 до 100 (включительно) из 3 строк и 2 столбцов.
even  = np.array(list(range(2,17,2))) #сохраните четные числа от 2 до 16 (включительно)
mix = np.random.permutation(even)   #Перемешайте числа в mix так, чтобы массив изменился
select = np.random.choice(even,size = 3,replace = False) #Получите из even 3 числа без повторений.
triplet =np.random.permutation(select) # перемешанные значения из массива select (сам select измениться не должен)


print(triplet)