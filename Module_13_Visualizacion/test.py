import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#amazon_data = pd.read_csv('data/amazon_com.csv')
amazon_data = pd.read_csv('Module_13/data/ae_com.csv')
amazon_data.head()

def replace_url(brand_name):
    if 'ref=' in brand_name:
        if 'Calvin' in brand_name:
            return 'Calvin-Klein'
        elif 'Wacoal' in brand_name:
            return 'Wacoal'
        else:
            return 'b.tempt'
    else:
        return brand_name
    
amazon_data['brand_name'] = amazon_data['brand_name'].apply(replace_url)
amazon_data['price'] = amazon_data['price'].str.replace('USD', '').astype('float64')
#amazon_data['brand_name'].unique()

#test_amazon = amazon_data.loc[:,['brand_name','price','product_category']]


#print(test_amazon.head(3))

# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))
# barplot1 = sns.barplot(
#     data=amazon_data,
#     x='brand_name',
#     y='price',
#     orient='v',
#     ax = axes[0],
#     ci=None
# )
# barplot1.tick_params(axis='x', rotation=70);
# barplot1.set_title('Средняя стоимость товаров по брендам', fontsize=16);
# barplot1.set_xlabel('Название бренда', fontsize=14);
# barplot1.set_ylabel('Средняя цена', fontsize=14);
# barplot1.grid()

barplot2 = sns.barplot(
    #data=amazon_data,
    data=amazon_data,
    x='brand_name',
    y='price',
    hue='product_category',
    orient='v',
    #ax = axes[1],
    #ci=None,
    legend=False,
    errorbar=None,
    dodge=False
)
barplot2.tick_params(axis='x', rotation=70);
barplot2.set_title('Средняя стоимость товаров по брендам и категориям', fontsize=16);
barplot2.set_xlabel('Название бренда', fontsize=14);
barplot2.set_ylabel('Средняя цена', fontsize=14);
barplot2.grid()


plt.show()