# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 00:55:31 2025

@author: tomfi
"""
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class FeaturePredictor(BaseEstimator, TransformerMixin):
    def __init__(self, temperature_model, illuminance_model):
        self.temperature_model = temperature_model
        self.illuminance_model = illuminance_model
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Predict temperature and illuminance using the first model
        temperature_pred = self.temperature_model.predict(X)
        illuminance_pred = self.illuminance_model.predict(X)
        return pd.DataFrame({'temperature': temperature_pred, 'illuminance': illuminance_pred})