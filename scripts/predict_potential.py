import sys  
import joblib  
import pandas as pd  
import numpy as np  
import json  
from sklearn.cluster import KMeans  

# Load các tài nguyên cần thiết
scaler = joblib.load("models/scaler_potential.pkl")  
model = joblib.load("models/model_potential.pkl")  
label_encoders = joblib.load("models/label_encoders.pkl")  
data = pd.read_csv("data_behavior_expand_x30.csv")  

# Hàm kiểm tra cột 'Potential Customer'
def add_potential_customer_column():  
    if 'Potential Customer' not in data.columns or data['Potential Customer'].isnull().any():  
        X_class = data[['Age', 'Gender', 'Purchase Amount (USD)', 'State', 'Subscription Status', 'Frequency of Purchases']].copy()
        for col in X_class.columns:  
            if col in label_encoders and col != 'Purchase Amount (USD)':  
                X_class[col] = label_encoders[col].transform(X_class[col])  
        X_scaled_class = scaler.transform(X_class)  
        kmeans = KMeans(n_clusters=2, random_state=42)  
        data['Segment'] = kmeans.fit_predict(X_scaled_class)  
        centroids = kmeans.cluster_centers_  
        distances = np.linalg.norm(X_scaled_class - centroids[kmeans.labels_], axis=1)  
        threshold = np.median(distances)  
        data['Potential Customer'] = np.where(distances < threshold, 'Tiềm năng', 'Không tiềm năng')  

add_potential_customer_column()

# Hàm dự đoán phân khúc khách hàng
def predict_potential(age, gender, purchase_amount, state, subscription_status, frequency_of_purchases):  
    try:  
        new_customer_data = pd.DataFrame({  
            'Age': [age],  
            'Gender': [gender],  
            'Purchase Amount (USD)': [purchase_amount],  
            'State': [state],  
            'Subscription Status': [subscription_status],  
            'Frequency of Purchases': [frequency_of_purchases]  
        })  

        # Mã hóa dữ liệu cho các cột không phải 'Purchase Amount (USD)'
        for col in ['Age', 'Gender', 'State', 'Subscription Status', 'Frequency of Purchases']:  
            if col in label_encoders:  
                if new_customer_data[col][0] not in label_encoders[col].classes_:  
                    raise ValueError(f"Value '{new_customer_data[col][0]}' not in label encoder for column '{col}'")  
                new_customer_data[col] = label_encoders[col].transform(new_customer_data[col])  

        # Chuẩn hóa dữ liệu mới
        new_customer_data_scaled = scaler.transform(new_customer_data)  

        # Dự đoán phân khúc khách hàng  
        predicted_potential = model.predict(new_customer_data_scaled)  
        predicted_potential_name = label_encoders['Potential Customer'].inverse_transform(predicted_potential)[0]  

        result = {  
            "predicted_potential": predicted_potential_name  
        }  
        print(json.dumps(result))  

    except Exception as e:  
        print(json.dumps({"error": str(e)}))  

if __name__ == "__main__":  
    try:  
        age = int(sys.argv[1])  
        gender = sys.argv[2]  
        purchase_amount = float(sys.argv[3])  
        state = sys.argv[4]  
        subscription_status = sys.argv[5]  
        frequency_of_purchases = sys.argv[6]  
        predict_potential(age, gender, purchase_amount, state, subscription_status, frequency_of_purchases)  
    except Exception as e:  
        print(json.dumps({"error": str(e)}))  
