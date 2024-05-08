from rbtree_fixed import Node, Tree
import streamlit as st
from pydot import *
from graphviz import *
import time

st.set_page_config(
    page_title="RedBlackTree",
)

session = st.session_state

if 'tree' not in session:
    session.tree = Tree()

if 'inserted_values' not in session:
    session.inserted_values = []

if 'session_iteration' not in session:
    session.session_iteration = 0

if 'deleting_values' not in session:
    session.deleting_values = []

st.title('RedBlackTree')
sidebar = st.sidebar


# sidebar.subheader('Поиск')
# value = sidebar.text_input(label='Введите число:', key='search_field', label_visibility='collapsed')
# if sidebar.button(label='Найти', key='search_button', use_container_width=True) and value:
#     node = session.tree.search_node(session.tree.root, int(value))
#     if node:
#         st.success(f'Найден узел {value}')
#     else:
#         st.warning(f'Не найдено: {value}')


sidebar.subheader('Вставка')
sidebar.text_input(label='Введите числа:', key='insert_field', label_visibility='collapsed')
def clear_insert_text():
    session.new_values = session.insert_field
    session["insert_field"] = ""
sidebar.button(label='Вставить', key='insert_button', on_click=clear_insert_text, use_container_width=True)


sidebar.subheader('Удаление')
sidebar.text_input(
    label='Введите числа:',
    key='values2delete',
    label_visibility='collapsed'
)
def clear_delete_text():
    session.deleting_values = session.values2delete
    session["values2delete"] = ""
sidebar.button(label='Удалить', key='delete_button', on_click=clear_delete_text, use_container_width=True)

if session.insert_button:
    try:
        new_values = [int(value) for value in 
                      session.new_values.split()]
    except Exception as e:
        new_values = None

    correct_values = []
    wrong_values = []
    for value in new_values:
        try:
            session.tree.insert(value)
            session.inserted_values.append(value)
            correct_values.append(value)
        except Exception:
            wrong_values.append(value)
    if correct_values:
        st.success(f'Были добавлены: {correct_values}')
    if wrong_values:
        st.warning(f'Ошибка: {wrong_values}')

if session.delete_button:
    try:
        values2delete = [int(value) for value in 
            session.deleting_values.split()]
    except Exception as e:
        values2delete = None
        st.error(f'Неправильный ввод: {e}')

    correct_values = []
    wrong_values = []
    for value in values2delete:
        try:
            session.tree.delete_node(session.tree.root, value)
            session.inserted_values.remove(value)
            correct_values.append(value)
        except ValueError:
            wrong_values.append(value)
    if correct_values:
        st.success(f'Были удалены: {correct_values}')
    if wrong_values:
        st.warning(f'Не были удалены: {wrong_values}')

if session.inserted_values:
    tree = session.tree
    dot = Digraph()
    dot.attr('node', fontcolor = 'white')
    tree.visualize_binary_tree_dot(tree.root, dot)
    st.graphviz_chart(dot.source)
