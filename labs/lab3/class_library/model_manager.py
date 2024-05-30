import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from imblearn.under_sampling import NearMiss

class ModelManager:
    
    def __init__(self, models:dict):
        self.current_model = None
        self.parameters = None
        self.ratio = None
        self.models = models
         
    def set_model(self, model_name:str):
        self.current_model = self.models[model_name][0]
        self.parameters = self.models[model_name][1]
        self.model_type = self.models[model_name][2]
        if self.model_type == 'classificator':
            self.ratio = self.class_ratio

        elif self.model_type == 'regressor':
            self.ratio = self.reg_ratio

    def fit(self, X, y):
        if self.model_type == 'classificator':
            X, y = self.balance_classes(X, y)
            print(f'succesful imbalance removing')
            
        self.current_model.fit(X, y)

    def predict(self, X, y):     
        predict = self.current_model.predict(X)
        return predict, self.ratio(y, predict)

    def class_ratio(self, y_test, predict) -> dict:
        return {'Classification report' : classification_report(y_test, predict), 'F1 score' : f1_score(y_test, predict)}

    def reg_ratio(self, y_test, predict) -> dict:
        MAE = mean_absolute_error(y_test, predict)
        MSE = mean_squared_error(y_test, predict)
        MAPE = mean_absolute_percentage_error(y_test, predict)
        R2 = r2_score(y_test, predict)

        return {'MAE' : MAE, 'MSE' : MSE, 'MAPE': MAPE, 'R2' : R2}
            
    def balance_classes(self, X, y):
        nm = NearMiss()
        X_res, y_res = nm.fit_resample(X, y)
        return X_res, y_res


                




        

