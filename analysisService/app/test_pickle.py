# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 00:22:00 2025

@author: tomfi
"""
import pickle

# Load the model using Pickle
with open('model.pkl', 'rb') as file:
    loaded_model_pickle = pickle.load(file)