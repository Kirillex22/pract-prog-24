import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
import scipy.stats as stats


class DataPreparer:
    def __init__(self):
        self.data = None
        self.X = None
        self.y = None
        self.ord_encoder = OrdinalEncoder()

    def load_data(self, raw_data):
        self.data = raw_data
        self.st_sc = StandardScaler()

    def remove_trash(self):
        self.data.dropna(inplace = True)
        self.data.drop_duplicates(inplace = True)

    def remove_predictors(self, names_of_predictors):
        self.data.drop(names_of_predictors, axis = 1, inplace = True)

    def encode_categorial(self, names_of_predictors):
        ct = ColumnTransformer(transformers=[
        ('ord', self.ord_encoder, names_of_predictors)
        ])
        ct.set_output(transform='pandas')
        encoded_features = ct.fit_transform(self.data)
        self.data.drop(names_of_predictors, axis = 1, inplace = True)
        self.data = pd.concat(
            [
                self.data.reset_index(drop = True), 
                encoded_features.reset_index(drop = True)
            ], axis = 1
        )

    def remove_anomaly(self, names_of_predictors):
        z = np.abs(stats.zscore(self.data[names_of_predictors]))
        self.data[names_of_predictors] = self.data[names_of_predictors][(z<3).all(axis=1)]

    def get_splitted(self, target, test_size = 0.2):
        y = self.data[target].to_numpy()
        X = self.standartisate(
            self.data.drop([target], axis=1).to_numpy()
        )
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        return X_train, X_test, y_train, y_test

    def standartisate(self, X):
        return self.st_sc.fit_transform(X)

    def show_data(self):
        st.write(self.data.head(5))

    def get_features(self):
        return self.data.columns.to_list()

    def get_data(self):
        return self.data








        



