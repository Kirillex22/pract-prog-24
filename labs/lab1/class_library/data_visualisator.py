import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualisator:

    def __init__(self):
        self.data = None
        self.features = None

    def load_data(self, data):
        self.data = data
        self.features = data.columns.to_list()
            
    def boxplot(self, ft):
        st.title("Boxplot")    
        plt.figure(figsize=(10, 6))
        sns.boxplot(
            x = self.data[ft], color="orange", linewidth = 1.5
        )
        st.pyplot(plt)


    def displot(self, ft):
        st.title("Диаграмма плотности распределения")    
        plt.figure(figsize=(10, 6))
        sns.displot(data=self.data, x=ft, kind="kde")
        st.pyplot(plt)

    def show_displacement(self):
        ft = st.selectbox("Признаки", self.features)
        if ft is not None:
            self.boxplot(ft)
            self.displot(ft)
        
        
