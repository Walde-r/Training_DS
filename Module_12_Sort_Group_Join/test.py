import pandas as pd

melb_data = pd.read_csv('Module_12/data/melb_data_fe.csv')
melb_ds = melb_data.copy()



unique_list = []

for col in melb_ds.columns:
    item = (col, melb_ds[col].nunique(), melb_ds[col].dtypes)
    unique_list.append(item)

uniq_df = pd.DataFrame(unique_list,
                       columns=['Col_Name','Uniq_Val','Type_Name']).sort_values(by=['Uniq_Val'])


l_not_col = ['Date', 'Rooms', 'Bedroom', 'Bathroom', 'Car']

for item in unique_list:
    if item[0] not in l_not_col:
        if item[1] < 150:
            print(item)