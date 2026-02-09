import pandas as pd
import xgboost as xgb
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from django.conf import settings

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'food_data.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'freshness_xgb.json')
ENCODER_PATH = os.path.join(BASE_DIR, 'models', 'encoders.pkl')

def train_model():
    print(f"Loading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print("❌ Error: food_data.csv not found in ml_service/data/")
        return

    df = pd.read_csv(DATA_PATH)

    # 1. Define Features
    # Based on your CSV columns: storage_time, time_since_cooking, storage_condition, etc.
    categorical_cols = ['storage_condition', 'container_type', 'food_type', 'moisture_type', 'cooking_method', 'texture', 'smell']
    numerical_cols = ['storage_time', 'time_since_cooking']
    target_col = 'freshness_level'

    # 2. Preprocessing (Label Encoding)
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    
    # Encode Target (Fresh/Spoiled -> 0, 1, 2)
    target_le = LabelEncoder()
    df[target_col] = target_le.fit_transform(df[target_col])
    encoders['target'] = target_le

    # 3. Train XGBoost
    X = df[categorical_cols + numerical_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training XGBoost Model...")
    model = xgb.XGBClassifier(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5, 
        objective='multi:softprob',  # For multi-class classification
        num_class=len(target_le.classes_)
    )
    model.fit(X_train, y_train)

    # 4. Save Artifacts
    os.makedirs(os.path.join(BASE_DIR, 'models'), exist_ok=True)
    model.save_model(MODEL_PATH) # XGBoost saves as JSON efficiently
    joblib.dump(encoders, ENCODER_PATH)
    
    print(f"✅ Model saved to {MODEL_PATH}")
    print(f"✅ Encoders saved to {ENCODER_PATH}")

if __name__ == "__main__":
    train_model()