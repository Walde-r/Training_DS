import pandas as pd

def delete_columns(df, col=[]):
    """которая удаляет столбцы из DataFrame возвращает новую таблицу. 
    Если одного из указанных столбцов не существует в таблице, то функция должна возвращать None
_

    Args:
        df (_type_): DataFrame
        col (list, optional): Columns. Defaults to [].
    """
    #for column in col:
    try:
        df = df.drop(col, axis = 1)
        return df
    except KeyError:
        return None


customer_df = pd.DataFrame({
            'number': [0, 1, 2, 3, 4],
            'cust_id': [128, 1201, 9832, 4392, 7472],
            'cust_age': [13, 21, 19, 21, 60],
            'cust_sale': [0, 0, 0.2, 0.15, 0.3],
            'cust_year_birth': [2008, 2000, 2002, 2000, 1961],
            'cust_order': [1400, 14142, 900, 1240, 8430]
        })

print(delete_columns(customer_df,['number']))