import sys
import joblib
import pandas as pd
import numpy as np

# Load models and scalers
scaler = joblib.load("models/scaler_potential.pkl")
model = joblib.load("models/model_potential.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

def predict_potential(age, gender, purchase_amount, state, subscription_status, frequency_of_purchases):
    try:
        # Input data
        new_customer_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            'Purchase Amount (USD)': [purchase_amount],
            'State': [state],
            'Subscription Status': [subscription_status],
            'Frequency of Purchases': [frequency_of_purchases]
        })

        # Encode the data
        for col in ['Age', 'Gender', 'State', 'Subscription Status', 'Frequency of Purchases']:
            new_customer_data[col] = label_encoders[col].transform(new_customer_data[col])

        # Scale the data
        new_customer_data_scaled = scaler.transform(new_customer_data)

        # Predict
        predicted_potential = model.predict(new_customer_data_scaled)
        predicted_potential_name = label_encoders['Potential Customer'].inverse_transform(predicted_potential)
        
        print(predicted_potential_name[0])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    age = int(sys.argv[1])
    gender = sys.argv[2]
    purchase_amount = float(sys.argv[3])
    state = sys.argv[4]
    subscription_status = sys.argv[5]
    frequency_of_purchases = sys.argv[6]
    predict_potential(age, gender, purchase_amount, state, subscription_status, frequency_of_purchases)
