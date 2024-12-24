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
├── data_behavior_expand.csv  # Dataset gốc

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

Mở và chạy file `Final_BI_V2.ipynb` để huấn luyện mô hình và lưu các file sau:

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
    "state": "Kentucky",
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
      "age": 40,
      "gender": "Female",
      "purchase_amount": 77,
      "state": "Minnesota",
      "subscription_status": "No",
      "frequency_of_purchases": "Weekly"
    }
    ```

## 📝 BÁO CÁO CHI TIẾT DỰ ÁN DỰ ĐOÁN XU HƯỚNG THỜI TRANG VÀ PHÂN LOẠI KHÁCH HÀNG

### 🚀 1. GIỚI THIỆU DỰ ÁN

#### 📌 1.1 Bối Cảnh & Vấn Đề Đặt Ra

- #### Ngành thời trang là một trong những lĩnh vực phát triển nhanh nhất trên thế giới, nhưng cũng là lĩnh vực dễ bị ảnh hưởng bởi xu hướng tiêu dùng và hành vi khách hàng

- #### Các doanh nghiệp bán lẻ thường gặp khó khăn trong việc

  - #### Dự đoán sản phẩm bán chạy trong từng mùa, từng khu vực

  - #### Phân loại khách hàng để tập trung vào những đối tượng tiềm năng nhất

- #### Việc sử dụng trí tuệ nhân tạo (AI) và học máy (Machine Learning) giúp giải quyết bài toán này một cách hiệu quả và tối ưu

#### 📌 1.2 Mục Tiêu Dự Án

- #### `Mục Tiêu 1:` Dự đoán sản phẩm thời trang phù hợp cho từng đối tượng khách hàng

- #### `Mục Tiêu 2:` Phân loại khách hàng thành "Tiềm năng" và "Không tiềm năng" dựa trên hành vi và thông tin cá nhân

- #### `Mục Tiêu 3:` Tích hợp API vào các nền tảng thương mại điện tử và CRM để tự động hóa quy trình

### 🎯 2. TÍNH NĂNG CHÍNH CỦA API

#### ✅ 2.1 API Dự Đoán Xu Hướng Thời Trang `(/predict-trend)`

- #### `Chức năng:` Dự đoán sản phẩm thời trang phù hợp dựa trên dữ liệu khách hàng

- #### `💡 Ứng Dụng Thực Tế:`

  - #### Gợi ý sản phẩm phù hợp trên trang web thương mại điện tử

  - #### Phân tích xu hướng mua sắm theo mùa và địa phương

#### ✅ 2.2 API Phân Loại Khách Hàng `(/predict-potential)`

- #### `Chức năng:` Phân loại khách hàng thành `"Tiềm năng"` và `"Không tiềm năng"` dựa trên thông tin mua sắm và hành vi tiêu dùng

- #### `💡 Ứng Dụng Thực Tế:`

  - #### Xác định khách hàng tiềm năng cho các chiến dịch khuyến mãi

  - #### Phân bổ ngân sách marketing hiệu quả

### 💼 3. ĐỐI TƯỢNG SỬ DỤNG API

| Đối tượng               | Ứng dụng                                        | Lợi ích                          |
| ----------------------- | ----------------------------------------------- | -------------------------------- |
| Doanh Nghiệp Thời Trang | Dự đoán xu hướng sản phẩm, phân loại khách hàng | Tăng doanh thu, tối ưu kho hàng  |
| Đội Ngũ Marketing       | Tập trung vào khách hàng tiềm năng              | Tối ưu chi phí quảng cáo         |
| Sàn Thương Mại Điện Tử  | Gợi ý sản phẩm cá nhân hóa                      | Cải thiện trải nghiệm khách hàng |
| CRM/ERP Systems         | Phân tích và theo dõi hành vi khách hàng        | Tăng hiệu suất bán hàng          |

### 📊 4. LỢI ÍCH CỦA API

1. Dự đoán xu hướng sản phẩm chính xác cao.

2. Tự động phân loại khách hàng theo nhóm tiềm năng.

3. Giảm chi phí marketing thông qua việc tối ưu đối tượng mục tiêu.

4. Tích hợp dễ dàng với các hệ thống CRM, ERP.

5. API có khả năng mở rộng, phù hợp cho doanh nghiệp lớn và nhỏ.

### 🔄 5. QUY TRÌNH HOẠT ĐỘNG CỦA API

`Khách Hàng → API /predict-trend → Python Backend → Machine Learning Model → Phân Tích Dữ Liệu → Dự Đoán Sản Phẩm → Trả Kết Quả`

`Khách Hàng → API /predict-potential → Python Backend → Machine Learning Model → Phân Tích Hành Vi → Phân Loại → Trả Kết Quả`
