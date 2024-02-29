import streamlit as st
import pandas as pd
import numpy as np
import statistics
from sklearn.linear_model import Perceptron, SGDRegressor
import sys

sys.path.append('..')

from class_library.model_manager import ModelManager
from class_library.data_visualisator import DataVisualisator
from class_library.data_preparer import DataPreparer

mm = ModelManager({
    'perceptron' : [Perceptron(), {
        'penalty' : ['l2','l1','elasticnet'],
        'alpha' : np.arange(0.001, 0.1, 0.01)
        }],
    'sgdregressor' : [SGDRegressor(), {
        'penalty' : ['l2','l1','elasticnet'],
        'loss':  ['squared_error', 'huber', 'epsilon_insensitive', 
        'squared_epsilon_insensitive'], 
        'alpha' : np.arange(0.001, 0.1, 0.01)
        }]
    })

dv = DataVisualisator()
dp = DataPreparer()

def data_loader():
    data = st.file_uploader("Загрузите датасет в формате *.csv", type="csv")
    if data is not None:
        data = pd.read_csv(data, sep = ';')
        dp.load_data(data)
        dv.load_data(data)
        return data

def model_change_manager():
    st.markdown("Ваш датасет:")
    st.write(data[:5])
         
    types = ["Классификация *(обучение на модели Perceptron)", "Регрессия *(обучение на модели SGDRegressor)"]   
    current_type = st.selectbox("Выберите задачу ML", types, index=None)
               
    if current_type is not None:
        if current_type == types[0]:
            mm.set_model('perceptron', 'classificator')

        elif current_type == types[1]:
            mm.set_model('sgdregressor', 'regressor')

        preparing_manager()
            
def predict_manager():
    target = st.text_input("Введите метку целевого признака")
    predict_manager_chbox = st.checkbox('Обучить модель и получить метрики качества')
    if (target != "" and predict_manager_chbox):
        X_train, X_test, y_train, y_test = dp.get_splitted(target)
        mm.fit(X_train, y_train)
        result, report = mm.predict(X_test, y_test)
        st.json(report)
        st.write(result)

def endcode_categorial_features():
    categorial_encoder_chbox = st.checkbox('Есть ли в датасете предикторы, содержащие нечисловые категориальные значения?')
    st.write(data[:5])
    if (categorial_encoder_chbox):   
        fts_to_prepare = st.multiselect(
            'Выбор предикторов c кат. значениями', dv.features,
            max_selections=len(dv.features)
        )
        sub_chbox1 = st.checkbox('Закодировать признаки')
        if (len(fts_to_prepare) != 0 and sub_chbox1):
            dp.encode_categorial(fts_to_prepare)

def clear_anomaly():
    sub_chbox2 = st.checkbox('Есть ли в датасете выбросы? Взгляните на диаграммы и внесите в список, если таковые имеются')
    displacement_chbox = st.checkbox('Показать диаграммы')

    if (displacement_chbox):
        dv.show_displacement()
                
    if (sub_chbox2):
        fts_to_fix = st.multiselect(
            'Выбор предикторов с выбросами', dv.features,
            max_selections=len(dv.features)
        )
        sub_chbox3 = st.checkbox('Удалить выбросы')
        if (len(fts_to_fix) != 0 and sub_chbox3):
            dp.remove_anomaly(fts_to_fix)

def clear_trash():
    dp.remove_trash()

def preparing_manager():
    types = ["Да (указание целевого признака и получение результата)", "Нет (переход к обработке)"]   
    current_type = st.selectbox("Был ли ваш датасет подготовлен для решения задачи машинного обучения?", types, index=None)

    if current_type is not None:
        if current_type == types[0]:
            predict_manager()

        elif current_type == types[1]:
            clear_trash()
            endcode_categorial_features()
            clear_anomaly()
            sub_chbox4 = st.checkbox('Перейти к указанию целевого признака и получению результатов')  
            if (sub_chbox4):
                predict_manager()

st.title("Предварительная обработка данных и получение предикта")
data = data_loader()
main_chbox = st.checkbox('Перейти к моделям')
if(main_chbox):
    model_change_manager()