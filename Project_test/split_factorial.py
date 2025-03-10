from math import factorial

def decompose_factorial(in_n):
    f_n = factorial(in_n)
    start_del = 2
    
    def get_mesg(sps_del):
        #формируется итоговое сообщение
        res_msg = ''
        l_cnt = 0
        l_set = set(sps_del)
        l_operand = ''
        i = 0
        
        for elem in l_set:
            l_cnt = sps_del.count(elem)
            if i != 0:
                l_operand = '*'    
            if l_cnt == 1:
                res_msg += f' {l_operand} {elem}'
            else:
                res_msg += f' {l_operand} {elem}^{l_cnt}'   
            i += 1    
        return f'{in_n}! =' + res_msg
        
    def split_mn(in_value, p_del):
        sps_del = []      
        for p_del in range(p_del, in_value+1):
            ostatok = in_value%p_del #цикл до тех пор пока не найден делитель который делит число без остатка
            next_val = in_value//p_del  #значение полученное от деления, используется в качестве делимого на следующем шаге  
        
            if ostatok == 0: #если делится без остатка
                sps_del.append(p_del)  #фиксируем делитель в списке
                if next_val != 1:   #если результат равен 1 то 
                    sps_del += split_mn(next_val,start_del)  #Переход к поиску следующего делителя
                    break
            else:
                p_del +=1
                        
        return sps_del  #вернуть сформированный список

    print(get_mesg(split_mn(f_n, start_del)))

decompose_factorial(25)



#25! = 2^22 * 3^10 * 5^6 * 7^3 * 11^2 * 13 * 17 * 19 * 23