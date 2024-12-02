const path = require("path");
const { PythonShell } = require("python-shell");

const predictTrend = (req, res) => {
  const { age, gender, category, state, season } = req.body;

  // Đường dẫn tới script Python
  const scriptPath = path.join(__dirname, "../scripts/predict_trend.py");

  // Tham số truyền vào Python
  const options = {
    args: [age, gender, category, state, season],
  };

  // Chạy script Python
  PythonShell.run(scriptPath, options, (err, results) => {
    if (err) {
      console.error("Error executing Python script:", err); // In lỗi thực thi
      return res.status(500).json({ error: err.message });
    }

    // Kiểm tra và in kết quả từ Python
    console.log("Python script results:", results);

    try {
      // Kết quả từ Python trả về
      const output = JSON.parse(results[0]); // Phân tích JSON
      res.json(output);
    } catch (parseError) {
      console.error("JSON Parse Error:", parseError); // In ra lỗi phân tích JSON
      return res
        .status(500)
        .json({ error: "Unable to parse response from Python script." });
    }
  });
};

const predictPotential = (req, res) => {
  const {
    age,
    gender,
    purchaseAmount,
    state,
    subscriptionStatus,
    frequencyOfPurchases,
  } = req.body;

  // Đường dẫn tới script Python
  const scriptPath = path.join(__dirname, "../scripts/predict_potential.py");

  // Tham số truyền vào Python
  const options = {
    args: [
      age,
      gender,
      purchaseAmount,
      state,
      subscriptionStatus,
      frequencyOfPurchases,
    ],
  };

  // Chạy script Python
  PythonShell.run(scriptPath, options, (err, results) => {
    if (err) {
      console.error("Error executing Python script:", err); // In lỗi thực thi
      return res.status(500).json({ error: err.message });
    }

    // Kiểm tra và in kết quả từ Python
    console.log("Python script results:", results);

    try {
      // Kết quả từ Python trả về
      const output = JSON.parse(results[0]); // Phân tích JSON
      res.json(output);
    } catch (parseError) {
      console.error("JSON Parse Error:", parseError); // In ra lỗi phân tích JSON
      return res
        .status(500)
        .json({ error: "Unable to parse response from Python script." });
    }
  });
};

module.exports = { predictTrend, predictPotential };
