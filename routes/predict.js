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
      res.status(500).json({ error: err.message });
    } else {
      // Kết quả từ Python trả về
      const output = JSON.parse(results[0]);
      res.json(output);
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
      res.status(500).json({ error: err.message });
    } else {
      // Kết quả từ Python trả về
      const output = JSON.parse(results[0]);
      res.json(output);
    }
  });
};

module.exports = { predictTrend, predictPotential };
