import os
import joblib
import xgboost as xgb
import pandas as pd
import numpy as np

class FreshnessPredictor:
    _model = None
    _encoders = None

    @classmethod
    def _load_artifacts(cls):
        """Load model and encoders only once."""
        if cls._model is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, 'models', 'freshness_xgb.json')
            encoder_path = os.path.join(base_dir, 'models', 'encoders.pkl')

            # Load XGBoost
            cls._model = xgb.XGBClassifier()
            cls._model.load_model(model_path)
            
            # Load Encoders
            cls._encoders = joblib.load(encoder_path)

    @classmethod
    @staticmethod
    def predict(data):
        # ... (Your existing loading code) ...

        # 1. Create DataFrame for Model
        input_df = pd.DataFrame([data])
        
        # 2. Get Base Prediction from Model
        # (Assuming your model doesn't use 'temperature' natively yet)
        # We drop temperature before passing to model if the model wasn't trained on it
        model_input = input_df.drop(columns=['temperature'], errors='ignore')
        
        base_score = FreshnessPredictor.model.predict(model_input)[0] # e.g., 85%

        # 3. APPLY REAL-WORLD TEMPERATURE LOGIC 🌡️
        temp = data.get('temperature', 25)
        condition = data.get('storage_condition', 'outside')

        # If food is OUTSIDE and it is HOT
        if condition == 'room_temperature' or condition == 'outside':
            if temp > 35:
                base_score -= 20  # Heavy penalty for extreme heat
            elif temp > 30:
                base_score -= 10  # Moderate penalty for heat
            elif temp < 10:
                base_score += 5   # Bonus for cold weather (acts like a fridge)

        # Ensure score stays 0-100
        final_score = max(0, min(100, base_score))

        # 4. Determine Label
        if final_score > 70: label = "Fresh"
        elif final_score > 40: label = "Moderate"
        else: label = "Spoiled"

        return {
            "freshness_score": final_score,
            "freshness_label": label
        }