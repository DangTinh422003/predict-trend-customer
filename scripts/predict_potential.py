import sys
import pandas as pd
import joblib
import os

# Load models and encoders
script_dir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(script_dir, "../models/model_potential.pkl")
label_encoders_path = os.path.join(script_dir, "../models/label_encoders.pkl")
scaler_path = os.path.join(script_dir, "../models/scaler_potential.pkl")

model = joblib.load(model_path)
label_encoders = joblib.load(label_encoders_path)
scaler = joblib.load(scaler_path)

# Nhận tham số từ dòng lệnh
age, gender, purchase_amount, location, subscription_status, frequency_of_purchases = sys.argv[1:]

new_customer_data = pd.DataFrame({
    "Age": [int(age)],
    "Gender": [gender],
    "Purchase Amount (USD)": [float(purchase_amount)],
    "Location": [location],
    "Subscription Status": [subscription_status],
    "Frequency of Purchases": [frequency_of_purchases]
})

# Mã hóa dữ liệu
for col in new_customer_data.columns:
    if col not in ["Age", "Purchase Amount (USD)"] and col in label_encoders:
        new_customer_data[col] = label_encoders[col].transform(new_customer_data[col])

# Chuẩn hóa dữ liệu
new_data_scaled = scaler.transform(new_customer_data)

# Dự đoán
prediction = model.predict(new_data_scaled)
predicted_segment = label_encoders["Potential Customer"].inverse_transform(prediction)
print(predicted_segment[0])
