import numpy as np
import math
from scipy.stats import mode

class MyDecisionTree:
    
    def __init__(self, *args, metric = 'mse', max_depth = 3, min_samples_split = 2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.current_depth = 0
        
        if metric == 'gini':
            self.metric, self.leaf = self.gini, lambda y: mode(y)[0]
        elif metric == 'mse':
            self.metric, self.leaf = self.mse, lambda y: np.mean(y)
            
                    
    def fit(self, X, y):
        self.current_depth = 0
        self.X, self.y = X, y
        self.model = self.tree(X, y)
        print(self.model)     
            
    def tree(self, X, y):
        if(self.current_depth >= self.max_depth)|(self.X.shape[0] <= self.min_samples_split):
            return {'predict': self.leaf(y)}          

        optimal_split = self.splitter() 
        self.current_depth += 1

        left_indexes = self.X[:, optimal_split['index']] < optimal_split['value']     
        right_indexes = self.X[:, optimal_split['index']] >= optimal_split['value']
        
        left_X, left_y = self.X[left_indexes], self.y[left_indexes]
        right_X, right_y = self.X[right_indexes], self.y[right_indexes]        

        model = {
            'index': optimal_split['index'],
            'value': optimal_split['value'],
            'metric': optimal_split['metric'],
            'left_child': self.tree(left_X, left_y),
            'right_child': self.tree(right_X, right_y)
        }       
        return model
        

    def splitter(self):
        optimal_split = {'metric': math.inf, 'index': 0, 'value': 0}     
        
        for col_index in range(self.X.shape[1]):
            split_values = np.unique(self.X[:, col_index])     
            
            for split_value in split_values:
                metric = self.metric([
                    self.y[self.X[:, col_index] < split_value], 
                    self.y[self.X[:, col_index] >= split_value]
                ])
                                 
                if metric < optimal_split['metric']:
                    optimal_split['metric'], optimal_split['index'], optimal_split['value'] = metric, col_index, split_value
        
        return optimal_split


    def gini(self, y):
        f = lambda y: len(y)*(1 - np.sum((np.bincount(y) / len(y))**2))    
        return (f(y[0]) + f(y[1])) / (len(y[0]) + len(y[1]))

    def mse(self, y):
        f = lambda y: len(y)*(np.mean((y - np.mean(y))**2))    
        return (f(y[0]) + f(y[1])) / (len(y[0]) + len(y[1]))

    def predict(self, X_test):
        predicts = []
        for x in X_test:
            predicts.append(self.finder(x, self.model))
                      
        return np.array(predicts)
   
        
    def finder(self, x, node): 
        f = lambda x: self.finder(x, node['left_child']) if (x[int(node['index'])] < node['value']) else self.finder(x, node['right_child'])   
        return (node['predict'] if ('predict' in node) else f(x))                    
