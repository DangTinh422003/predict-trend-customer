import sys
import joblib
import pandas as pd
import numpy as np
import json  # Thêm thư viện json

# Load models and scalers
scaler = joblib.load("models/scaler_trend.pkl")
model = joblib.load("models/model_trend.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")
data = pd.read_csv("data_behavior_expand_x30.csv")

def calculate_preference_percentage(item_name, age, season, category):
    total = data[(data['Age'] == age) & (data['Season'] == season) & (data['Category'] == category)]
    filtered_customers = total[total['Item Purchased'] == item_name]
    
    if total.empty or filtered_customers.empty:
        return 0.0
    
    percentage = (filtered_customers.shape[0] / total.shape[0]) * 100
    return percentage

def predict_trend(age, gender, category, state, season):
    try:
        new_customer_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            'Category': [category],
            'State': [state],
            'Season': [season]
        })

        for col in ['Age', 'Gender', 'Category', 'State', 'Season']:
            new_customer_data[col] = label_encoders[col].transform(new_customer_data[col])

        new_customer_data_scaled = scaler.transform(new_customer_data)

        predicted_item = model.predict(new_customer_data_scaled)
        predicted_item_name = label_encoders['Item Purchased'].inverse_transform(predicted_item)[0]

        percentage = calculate_preference_percentage(predicted_item_name, age, season, category)
        
        result = {"predicted_item": predicted_item_name, "percentage": percentage}
        print(json.dumps(result))  # Trả về JSON hợp lệ
    except Exception as e:
        print(json.dumps({"error": str(e)}))  # Trả về lỗi dưới dạng JSON

if __name__ == "__main__":
    age = int(sys.argv[1])
    gender = sys.argv[2]
    category = sys.argv[3]
    state = sys.argv[4]
    season = sys.argv[5]
    predict_trend(age, gender, category, state, season)
