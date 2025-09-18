import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from comet_ml import Experiment



def get_API_KEY(p_Name_API):
    res_API = None
    with open('C:\\Users\\washe\\Documents\\SF_Training_DS\\me_token.txt', 'r') as f_API:
        for str in f_API:
            if p_Name_API + ":" in str:
                res_API = str[len(p_Name_API)+1:].strip()
                break

    return res_API



# Создаем эксперимент с помощью имеющегося API ключа
l_key_API = get_API_KEY('COMMET.ML')
if not l_key_API is None:
    experiment = Experiment(
        api_key=l_key_API,
        project_name='medical-appointment',
        workspace='walde-r',
    )
else:
    print('Не найден key_API для COMMET.ML')




experiment.log_graph()
