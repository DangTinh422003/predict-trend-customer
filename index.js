const express = require("express");
const bodyParser = require("body-parser");
const { exec } = require("child_process");
const path = require("path");

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Trend Prediction Endpoint
app.post("/predict-trend", (req, res) => {
  const { age, gender, category, state, season } = req.body;

  const scriptPath = path.join(__dirname, "scripts/predict_trend.py");
  const command = `python ${scriptPath} ${age} "${gender}" "${category}" "${state}" "${season}"`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: stderr });
    }
    res.json({ predicted_item: stdout.trim() });
  });
});

// Potential Prediction Endpoint
app.post("/predict-potential", (req, res) => {
  const {
    age,
    gender,
    purchase_amount,
    state,
    subscription_status,
    frequency_of_purchases,
  } = req.body;

  const scriptPath = path.join(__dirname, "scripts/predict_potential.py");
  const command = `python ${scriptPath} ${age} "${gender}" ${purchase_amount} "${state}" "${subscription_status}" "${frequency_of_purchases}"`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: stderr });
    }
    res.json({ predicted_potential: stdout.trim() });
  });
});

// Start Server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
