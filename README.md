# **Dự án Dự đoán Xu Hướng Thời Trang và Phân Khúc Khách Hàng**

## **Giới thiệu**

Dự án này sử dụng **Python** và **Node.js** để xây dựng API backend dự đoán:

1. **Xu hướng thời trang**: Dựa trên các thông tin đầu vào như tuổi, giới tính, mùa, v.v., để dự đoán sản phẩm thời trang mà khách hàng có khả năng mua.
2. **Phân khúc khách hàng**: Phân loại khách hàng thành "Tiềm năng" hoặc "Không tiềm năng" dựa trên các thông tin mua sắm.

API được xây dựng bằng **Express.js** và các mô hình học máy được huấn luyện bằng **scikit-learn**.

---

## **Cấu trúc dự án**

```plaintext
final_BI/
├── express-BE/                    # Backend Express.js
│   ├── index.js                   # Khởi động server
│   ├── routes/
│   │   └── predict.js             # Xử lý logic API
│   ├── scripts/
│   │   ├── predict_trend.py       # Script Python dự đoán xu hướng
│   │   ├── predict_potential.py   # Script Python dự đoán phân khúc
│   ├── models/                    # Mô hình và scaler
│   │   ├── model_trend.pkl
│   │   ├── model_potential.pkl
│   │   ├── scaler_trend.pkl
│   │   ├── scaler_potential.pkl
│   │   └── label_encoders.pkl
│   ├── package.json               # Khai báo dependencies của Node.js
├── Final_BI.ipynb                 # Notebook huấn luyện mô hình
├── shopping_behavior_updated.csv  # Dataset gốc

```

## **Cài đặt**

### **Yêu cầu hệ thống**

- **Node.js**: >= 18.x
- **Python**: >= 3.8
- **pip**: >= 20.0
- **npm**: >= 6.x

### **Hướng dẫn cài đặt**

#### 1. Clone dự án

```bash
git clone <repository-url>
cd final_BI
```

#### 2. Cài đặt các package cho Node.js

```bash
npm install
```

#### 3. Cài đặt các package cho Python

```bash
python3 -m venv venv
source venv/bin/activate # Trên Linux/MacOS
venv\Scripts\activate # Trên Windows
pip install pandas scikit-learn joblib
```

#### 4. Lưu mô hình và scaler

Mở và chạy file `Final_BI.ipynb` để huấn luyện mô hình và lưu các file sau:

- `model_trend.pkl`
- `model_potential.pkl`
- `scaler_trend.pkl`
- `scaler_potential.pkl`
- `label_encoders.pkl`

Các file này sẽ được lưu trong thư mục `express-BE/models`.

## **Cách chạy**

### **1. Khởi động server**

Di chuyển vào thư mục `express-BE` và chạy lệnh sau:

```bash
npm run dev
```

Server sẽ chạy tại địa chỉ http://localhost:3000.

## **Sử dụng các Endpoint**

### **Dự đoán xu hướng thời trang**

- **Endpoint**: `POST http://localhost:3000/predict-trend`
- **Mô tả**: Dự đoán sản phẩm thời trang mà khách hàng có khả năng mua dựa trên thông tin đầu vào.
- **Yêu cầu**:
  Gửi một request với body JSON chứa các trường sau:

  ```json
  {
    "age": 30,
    "gender": "Male",
    "category": "Clothing",
    "location": "Kentucky",
    "color": "Black",
    "season": "Spring"
  }
  ```

### **Dự đoán phân khúc khách hàng**

- **Endpoint**: `POST http://localhost:3000/predict-potential`
- **Mô tả**: Phân loại khách hàng thành "Tiềm năng" hoặc "Không tiềm năng" dựa trên thông tin mua sắm.
- **Yêu cầu**:
  - **Phương thức**: `POST`
  - **Headers**:
    - `Content-Type`: `application/json`
  - **Body** (JSON):

    ```json
    {
      "age": 44,
      "gender": "Female",
      "purchaseAmount": 77,
      "location": "Minnesota",
      "subscriptionStatus": "No",
      "frequencyOfPurchases": "Weekly"
    }
    ```
