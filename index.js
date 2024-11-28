const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { predictTrend, predictPotential } = require("./routes/predict");

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Endpoint cho dự đoán xu hướng thời trang
app.post("/predict-trend", predictTrend);

// Endpoint cho dự đoán phân khúc khách hàng
app.post("/predict-potential", predictPotential);

const PORT = 3000;
app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));
