import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import GridSearchCV

class ModelManager:
    
    def __init__(self, models:dict):
        self.current_model = None
        self.parameters = None
        self.ratio = None
        self.models = models
        
         
    def set_model(self, model_name:str, model_type:str):
        self.current_model = self.models[model_name][0]
        self.parameters = self.models[model_name][1]
        if model_type == 'classificator':
            self.ratio = self.class_ratio
        elif model_type == 'regressor':
            self.ratio = self.reg_ratio

    def fit(self, X, y):
        result = GridSearchCV(self.current_model, self.parameters).fit(X, y)
        self.current_model = result.best_estimator_

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



        

