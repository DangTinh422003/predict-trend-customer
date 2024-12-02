import sys
import joblib
import pandas as pd
import numpy as np

# Load models and scalers
scaler = joblib.load("models/scaler_trend.pkl")
model = joblib.load("models/model_trend.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

def predict_trend(age, gender, category, state, season):
    try:
        # Input data
        new_customer_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            'Category': [category],
            'State': [state],
            'Season': [season]
        })

        # Encode the data
        for col in ['Age', 'Gender', 'Category', 'State', 'Season']:
            new_customer_data[col] = label_encoders[col].transform(new_customer_data[col])

        # Scale the data
        new_customer_data_scaled = scaler.transform(new_customer_data)

        # Predict
        predicted_item = model.predict(new_customer_data_scaled)
        predicted_item_name = label_encoders['Item Purchased'].inverse_transform(predicted_item)
        
        print(predicted_item_name[0])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    age = int(sys.argv[1])
    gender = sys.argv[2]
    category = sys.argv[3]
    state = sys.argv[4]
    season = sys.argv[5]
    predict_trend(age, gender, category, state, season)
