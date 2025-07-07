import pandas as pd
import sweetviz as sv
import os


os.chdir('C:\\Users\\washe\\Documents\\SF_Training_DS\\EDA_Разведывательный анализ')


df = pd.read_csv('data/wine.zip')


report = sv.analyze(df)
report.show_html()
