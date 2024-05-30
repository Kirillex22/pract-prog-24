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
from models.decisiontree import *

mm = ModelManager({
    'decision_tree_reg' : [MyDecisionTree(), {}, 'regressor'],
    'decision_tree_class' : [MyDecisionTree(metric='gini'), {}, 'classificator']
    })

dv = DataVisualisator()
dp = DataPreparer()

def data_loader():
    seps = [',', ';']
    data = st.file_uploader("Загрузите датасет в формате *.csv", type="csv")
    sep = st.selectbox("Укажите разделитель, который используется в датасете", seps, index=None)
    if ((data is not None) and (sep is not None)):
        data = pd.read_csv(data, sep = sep)
        dp.load_data(data)

def data_converter(data):
    return data.to_csv().encode('utf-8')

def model_change_manager():
    st.markdown("Ваш датасет:")
    dp.show_data()
         
    types = ["DTC (классификация)", "DTR (регрессия)"]   
    current_type = st.selectbox("Выберите задачу ML", types, index=None)
               
    if current_type is not None:
        if current_type == types[0]:
            mm.set_model('decision_tree_class')

        elif current_type == types[1]:
            mm.set_model('decision_tree_reg')

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
        st.download_button(
            label="Скачать обработанный датасет",
            data=data_converter(dp.get_data()),
            file_name='prepared.csv',
            mime='text/csv',
        )

def delete_features():
    delete_feature_chbox = st.checkbox('Есть ли в датасете столбцы, которые необходимо удалить?')
    dp.show_data()
    if (delete_feature_chbox):   
        fts_to_delete= st.multiselect(
            'Выбор предикторов для удаления', dp.get_features(),
            max_selections=len(dp.get_features())
        )
        sub_chbox = st.checkbox('Удалить столбцы')
        if (len(fts_to_delete) != 0 and sub_chbox):
            dp.remove_predictors(fts_to_delete)
            dp.show_data()

def endcode_categorial_features():
    categorial_encoder_chbox = st.checkbox('Есть ли в датасете предикторы, содержащие нечисловые категориальные значения?')
    dp.show_data()
    if (categorial_encoder_chbox):   
        fts_to_prepare = st.multiselect(
            'Выбор предикторов c кат. значениями', dp.get_features(),
            max_selections=len(dp.get_features())
        )
        sub_chbox = st.checkbox('Закодировать признаки')
        if (len(fts_to_prepare) != 0 and sub_chbox):
            dp.encode_categorial(fts_to_prepare)
            dp.show_data()

def clear_anomaly():
    sub_chbox = st.checkbox('Есть ли в датасете выбросы? Взгляните на диаграммы и внесите в список, если таковые имеются')
    displacement_chbox = st.checkbox('Показать диаграммы')
    dv.load_data(dp.get_data())
    if (displacement_chbox):
        dv.show_displacement()
                
    if (sub_chbox):
        fts_to_fix = st.multiselect(
            'Выбор предикторов с выбросами', dp.get_features(),
            max_selections=len(dp.get_features())
        )
        sub_chbox3 = st.checkbox('Удалить выбросы')
        if (len(fts_to_fix) != 0 and sub_chbox):
            dp.remove_anomaly(fts_to_fix)

def clear_trash():
    st.write("Пропуски успешно автоматически удалены")
    dp.remove_trash()
    dp.show_data()

def preparing_manager():
    types = ["Да (указание целевого признака и получение результата)", "Нет (переход к обработке)"]   
    current_type = st.selectbox("Был ли ваш датасет подготовлен для решения задачи машинного обучения?", types, index=None)

    if current_type is not None:
        if current_type == types[0]:
            predict_manager()

        elif current_type == types[1]:
            clear_trash()
            delete_features()
            endcode_categorial_features()
            clear_anomaly()
            sub_chbox4 = st.checkbox('Перейти к указанию целевого признака и получению результатов')  
            if (sub_chbox4):
                predict_manager()

st.title("Предварительная обработка данных и получение предикта")
data_loader()
main_chbox = st.checkbox('Перейти к моделям')
if(main_chbox):
    model_change_manager()