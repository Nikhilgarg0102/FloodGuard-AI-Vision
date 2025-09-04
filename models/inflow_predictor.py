import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
# Optional: use LSTM for more advanced prediction

class InflowPredictor:
    def __init__(self):
        self.model = GradientBoostingRegressor()

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_future):
        return self.model.predict(X_future)
