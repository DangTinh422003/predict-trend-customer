import sys
import pandas as pd
import joblib
import os

# Load models and encoders
script_dir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(script_dir, "../models/model_trend.pkl")
label_encoders_path = os.path.join(script_dir, "../models/label_encoders.pkl")
scaler_path = os.path.join(script_dir, "../models/scaler_trend.pkl")

model = joblib.load(model_path)
label_encoders = joblib.load(label_encoders_path)
scaler = joblib.load(scaler_path)

# Nhận tham số từ dòng lệnh
age, gender, category, location, color, season = sys.argv[1:]

new_customer_data = pd.DataFrame({
    "Age": [int(age)],
    "Gender": [gender],
    "Category": [category],
    "Location": [location],
    "Color": [color],
    "Season": [season]
})

# Mã hóa dữ liệu
for col in new_customer_data.columns:
    if col != "Age" and col in label_encoders:
        new_customer_data[col] = label_encoders[col].transform(new_customer_data[col])

# Chuẩn hóa dữ liệu
new_data_scaled = scaler.transform(new_customer_data)

# Dự đoán
prediction = model.predict(new_data_scaled)
predicted_item = label_encoders["Item Purchased"].inverse_transform(prediction)
print(predicted_item[0])
