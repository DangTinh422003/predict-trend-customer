const { spawn } = require("child_process");
const path = require("path");

const predictTrend = (req, res) => {
  const { age, gender, category, location, color, season } = req.body;

  const scriptPath = path.join(__dirname, "../scripts/predict_trend.py");
  const python = spawn("python", [
    scriptPath,
    age,
    gender,
    category,
    location,
    color,
    season,
  ]);

  let responseSent = false;

  python.stdout.on("data", (data) => {
    if (!responseSent) {
      responseSent = true;
      res.json({ predicted_item: data.toString().trim() });
    }
  });

  python.stderr.on("data", (data) => {
    if (!responseSent) {
      responseSent = true;
      res.status(500).json({ error: data.toString().trim() });
    }
  });

  python.on("close", (code) => {
    if (!responseSent) {
      responseSent = true;
      res
        .status(500)
        .json({ error: `Python process exited with code ${code}` });
    }
  });
};

const predictPotential = (req, res) => {
  const {
    age,
    gender,
    purchaseAmount,
    location,
    subscriptionStatus,
    frequencyOfPurchases,
  } = req.body;

  const scriptPath = path.join(__dirname, "../scripts/predict_potential.py");
  const python = spawn("python", [
    scriptPath,
    age,
    gender,
    purchaseAmount,
    location,
    subscriptionStatus,
    frequencyOfPurchases,
  ]);

  let responseSent = false;

  python.stdout.on("data", (data) => {
    if (!responseSent) {
      responseSent = true;
      res.json({ potential_customer: data.toString().trim() });
    }
  });

  python.stderr.on("data", (data) => {
    if (!responseSent) {
      responseSent = true;
      res.status(500).json({ error: data.toString().trim() });
    }
  });

  python.on("close", (code) => {
    if (!responseSent) {
      responseSent = true;
      res
        .status(500)
        .json({ error: `Python process exited with code ${code}` });
    }
  });
};

module.exports = { predictTrend, predictPotential };
