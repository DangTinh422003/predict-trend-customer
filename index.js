const express = require("express");
const bodyParser = require("body-parser");
const { exec } = require("child_process");
const path = require("path");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post("/predict-trend", (req, res) => {
  const { age, gender, category, state, season } = req.body;
  const scriptPath = path.join(__dirname, "scripts", "predict_trend.py");
  const command = `python ${scriptPath} ${age} "${gender}" "${category}" "${state}" "${season}"`;

  exec(command, (error, stdout, stderr) => {
    console.log("Python stdout:", stdout);
    console.log("Python stderr:", stderr);

    if (error) {
      return res.status(500).json({ error: stderr || error.message });
    }

    try {
      const cleanOutput = stdout.trim().split("\n").pop();
      const { percentage, ...rest } = JSON.parse(cleanOutput);
      res.json({ ...rest });
    } catch (parseError) {
      console.error("JSON Parse Error:", parseError.message);
      res.status(500).json({
        error: "Unable to parse response from Python script.",
        details: stdout.trim(),
      });
    }
  });
});

app.post("/predict-potential", (req, res) => {
  const {
    age,
    gender,
    purchase_amount,
    state,
    subscription_status,
    frequency_of_purchases,
  } = req.body;

  const scriptPath = path.join(__dirname, "scripts", "predict_potential.py");
  const command = `python ${scriptPath} ${age} "${gender}" ${purchase_amount} "${state}" "${subscription_status}" "${frequency_of_purchases}"`;

  exec(command, (error, stdout, stderr) => {
    console.log("Python stdout:", stdout);
    console.log("Python stderr:", stderr);

    if (error) {
      console.error("Error executing Python script:", error.message);
      return res.status(500).json({ error: stderr || error.message });
    }

    try {
      const cleanOutput = stdout.trim().split("\n").pop();
      const result = JSON.parse(cleanOutput);
      if (result.error) {
        console.error("Python Script Error:", result.error);
        return res.status(500).json({ error: result.error });
      }
      res.json(result);
    } catch (parseError) {
      console.error("JSON Parse Error:", parseError.message);
      res.status(500).json({
        error: "Unable to parse response from Python script.",
        details: stdout.trim(),
      });
    }
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
