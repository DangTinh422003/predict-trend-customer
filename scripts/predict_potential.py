import sys  
import joblib  
import pandas as pd  
import numpy as np  
import json  
from sklearn.cluster import KMeans  

scaler = joblib.load("models/scaler_potential.pkl")  
model = joblib.load("models/model_potential.pkl")  
label_encoders = joblib.load("models/label_encoders.pkl")  
data = pd.read_csv("data_behavior_expand_x30.csv")  

# In ra các lớp hợp lệ cho Subscription Status  
print("Subscription Status classes:", label_encoders['Subscription Status'].classes_)  

# Hàm để thêm cột 'Potential Customer' nếu chưa tồn tại  
def add_potential_customer_column():  
    if 'Potential Customer' not in data.columns or data['Potential Customer'].isnull().any():  
        print("Cột 'Potential Customer' chưa tồn tại hoặc có giá trị null. Đang tạo lại...")  

        # Chuẩn bị dữ liệu cho KMeans  
        X_class = data[['Age', 'Gender', 'Purchase Amount (USD)', 'State', 'Subscription Status', 'Frequency of Purchases']].copy()  
        
        # Mã hóa dữ liệu  
        for col in X_class.columns:  
            if col in label_encoders:  
                X_class[col] = label_encoders[col].transform(X_class[col])  

        # Chuẩn hóa dữ liệu  
        X_scaled_class = scaler.transform(X_class)  

        # Áp dụng KMeans  
        kmeans = KMeans(n_clusters=2, random_state=42)  
        data['Segment'] = kmeans.fit_predict(X_scaled_class)  

        # Tính khoảng cách Euclidean và thêm cột 'Potential Customer'  
        centroids = kmeans.cluster_centers_  
        distances = np.linalg.norm(X_scaled_class - centroids[kmeans.labels_], axis=1)  
        threshold = np.median(distances)  
        data['Potential Customer'] = np.where(distances < threshold, 'Tiềm năng', 'Không tiềm năng')  

# Gọi hàm để đảm bảo cột 'Potential Customer' tồn tại  
add_potential_customer_column()  

# Hàm tính tỷ lệ phần trăm  
def calculate_potential_percentage(age, gender, frequency, potential_name):  
    total = data[data['Potential Customer'] == potential_name]  
    
    if total.empty:  
        return {"age": 0.0, "gender": 0.0, "frequency": 0.0}  
    
    percentage_age = (total[total['Age'] == age].shape[0] / total.shape[0]) * 100  
    percentage_gender = (total[total['Gender'] == gender].shape[0] / total.shape[0]) * 100  
    percentage_frequency = (total[total['Frequency of Purchases'] == frequency].shape[0] / total.shape[0]) * 100  

    return {"age": percentage_age, "gender": percentage_gender, "frequency": percentage_frequency}  

# Hàm dự đoán phân khúc khách hàng  
def predict_potential(age, gender, purchase_amount, state, subscription_status, frequency_of_purchases):  
    try:  
        # Chuẩn bị dữ liệu đầu vào  
        new_customer_data = pd.DataFrame({  
            'Age': [age],  
            'Gender': [gender],  
            'Purchase Amount (USD)': [purchase_amount],  
            'State': [state],  
            'Subscription Status': [subscription_status],  
            'Frequency of Purchases': [frequency_of_purchases]  
        })  

        # Mã hóa dữ liệu  
        for col in ['Age', 'Gender', 'State', 'Subscription Status', 'Frequency of Purchases']:  
            if col in label_encoders:  
                if new_customer_data[col][0] not in label_encoders[col].classes_:  
                    raise ValueError(f"Value '{new_customer_data[col][0]}' not in label encoder for column '{col}'")  
                new_customer_data[col] = label_encoders[col].transform(new_customer_data[col])  
            else:  
                raise ValueError(f"Label encoder không tồn tại cho cột {col}")  

        # Chuẩn hóa dữ liệu  
        new_customer_data_scaled = scaler.transform(new_customer_data)  

        # Dự đoán phân khúc khách hàng  
        predicted_potential = model.predict(new_customer_data_scaled)  
        predicted_potential_name = label_encoders['Potential Customer'].inverse_transform(predicted_potential)[0]  

        # Tính toán tỷ lệ phần trăm  
        percentages = calculate_potential_percentage(age, gender, frequency_of_purchases, predicted_potential_name)  

        # Kết quả trả về  
        result = {"predicted_potential": predicted_potential_name, "percentages": percentages}  
        print(json.dumps(result))  # Xuất JSON hợp lệ  
    except Exception as e:  
        import traceback  
        print(json.dumps({"error": str(e), "details": traceback.format_exc()}))  # Trả về lỗi chi tiết dưới dạng JSON  

# Điểm bắt đầu  
if __name__ == "__main__":  
    try:  
        # Lấy tham số từ dòng lệnh  
        age = int(sys.argv[1])  
        gender = sys.argv[2]  
        purchase_amount = float(sys.argv[3])  
        state = sys.argv[4]  
        subscription_status = sys.argv[5]  
        frequency_of_purchases = sys.argv[6]  

        # Gọi hàm dự đoán  
        predict_potential(age, gender, purchase_amount, state, subscription_status, frequency_of_purchases)  
    except Exception as e:  
        import traceback  
        print(json.dumps({"error": str(e), "details": traceback.format_exc()}))