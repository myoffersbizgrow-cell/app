const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs-extra');
const convertRoute = require('./routes/convert');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static files
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Routes
app.use('/api', convertRoute);

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    tools: checkTools()
  });
});

// Check required tools
function checkTools() {
  const toolsPath = path.join(__dirname, 'tools');
  const required = ['apktool.jar', 'aapt2.exe', 'bundletool.jar', 'android.jar'];
  const available = {};
  
  required.forEach(tool => {
    available[tool] = fs.existsSync(path.join(toolsPath, tool));
  });
  
  return available;
}

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: err.message });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log('Tools status:', checkTools());
});