import sys
#sys.path.append('./')
import matplotlib.pyplot as plt
import streamlit as st
from pydot import *
from graphviz import *
from redblacktree import *

session = st.session_state

if 'tree' not in session:
    session.tree = RedBlackTree()

if 'inserted_values' not in session:
    session.inserted_values = []

if 'session_iteration' not in session:
    session.session_iteration = 0

st.title('Красно-чёрное дерево')

sidebar = st.sidebar
sidebar.title('Работа с деревом')

# вставка элемента
sidebar.subheader('Добавление')
sidebar.text_input(label='Введите числа:', key='insert_field', label_visibility='collapsed')
def clear_insert_text():
    session.new_value = session.insert_field
    session["insert_field"] = ""
sidebar.button(label='Добавить', key='insert_button', on_click=clear_insert_text, use_container_width=True)

# поиск элемента
sidebar.subheader('Поиск')
value = sidebar.text_input(label='Введите число:', key='search_field', label_visibility='collapsed')
if sidebar.button(label='Найти', key='search_button', use_container_width=True) and value:
    result = session.tree.search(int(value))
    if result == True:
        st.success(f'Найден узел {value}')
    else:
        st.warning(f'Не найдено: {value}')

# удаление элемента
sidebar.subheader('Удаление')
sidebar.text_input(
    label='Введите числа:',
    key='delete_field',
    label_visibility='collapsed'
)
def clear_delete_text():
    session.deleting_value = session.delete_field
    session["delete_field"] = ""
sidebar.button(label='Удалить', key='delete_button', on_click=clear_delete_text, use_container_width=True)

if session.insert_button:
    try:
        new_value = int(session.new_value)
    except ValueError as e:
        new_value = None
        st.error(f'Неправильный ввод: {e}')

    correct_values = []
    wrong_values = []
    try:
        session.tree.insert(new_value)
        session.inserted_values.append(new_value)
        correct_values.append(new_value)
    except ValueError:
        wrong_values.append(new_value)
    if correct_values:
        st.success(f'Успешно добавлено: {correct_values}')
    if wrong_values:
        st.warning(f'Не добавлено: {wrong_values}')

if session.delete_button:
    try:
        deleting_value = int(session.deleting_value)
    except ValueError as e:
        deleting_value = None
        st.error(f'Неправильный ввод: {e}')

    correct_values = []
    wrong_values = []
    try:
        session.tree.delete(deleting_value)
        session.inserted_values.remove(deleting_value)
        correct_values.append(deleting_value)
    except ValueError:
        wrong_values.append(deleting_value)
    if correct_values:
        st.success(f'Успешно удалено: {correct_values}')
    if wrong_values:
        st.warning(f'Не удалено: {wrong_values}')

if session.inserted_values:
    st.subheader(f'Добавленные значения значения: {sorted(session.inserted_values)}')
    tree = session.tree
    dot = Digraph()
    dot.attr('node', fontcolor = 'white')
    
    tree.visualize_binary_tree_dot(tree.root, dot)
    st.graphviz_chart(dot.source)