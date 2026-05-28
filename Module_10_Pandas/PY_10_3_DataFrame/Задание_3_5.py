import pandas as pd

income = [612, 516, 329, 158]
expenses = [136, 163, 250, 361]
years = [2017, 2018, 2019, 2020]

def create_companyDF(income, expenses, years):
    """возвращает DataFrame, составленный из входных данных со столбцами Income и Expenses и индексами, 
    соответствующими годам рассматриваемого периода."""
    
    res_DF = pd.DataFrame({'Income': income,
                           'Expenses': expenses},
                          index=years)

    return res_DF

def get_profit(df: pd.DataFrame, year: int):
    """возвращает разницу между доходом и расходом, записанными в таблице df, за год year.
    Примечание. Если информация за запрашиваемый год не указана в вашей таблице, вам необходимо вернуть None."""

    if type(year)==str:
        year = int(year)
    
    
    try:
        res_value = df.loc[year,'Income']-df.loc[year,'Expenses']
    except KeyError:
        res_value = None
    finally:
        return res_value

l_df = create_companyDF(income, expenses, years)
print(l_df)

print(get_profit(df=l_df,year=2018))