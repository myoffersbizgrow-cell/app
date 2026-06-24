const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs-extra');
const { v4: uuidv4 } = require('uuid');
const APKConverter = require('../services/apkConverter');

const router = express.Router();

// Multer config for file upload
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../uploads');
    await fs.ensureDir(uploadDir);
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}-${file.originalname}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 200 * 1024 * 1024 }, // 200MB max
  fileFilter: (req, file, cb) => {
    if (file.originalname.endsWith('.apk')) {
      cb(null, true);
    } else {
      cb(new Error('Only APK files are allowed'));
    }
  }
});

// Convert endpoint
router.post('/convert', upload.single('apk'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No APK file uploaded' });
    }

    const apkPath = req.file.path;
    const outputDir = path.join(__dirname, '../output', uuidv4());
    
    // Get versions from request
    const minSdk = parseInt(req.body.minSdk) || 21;
    const targetSdk = parseInt(req.body.targetSdk) || 33;
    const buildTools = req.body.buildTools || '30.0.3';

    console.log(`Converting: ${req.file.filename}`);
    console.log(`Min SDK: ${minSdk}, Target SDK: ${targetSdk}`);

    // Convert
    const converter = new APKConverter();
    const result = await converter.convert(apkPath, outputDir, {
      minSdk,
      targetSdk,
      buildTools
    });

    // Clean up uploaded APK
    await fs.remove(apkPath);

    // Send download link
    res.json({
      success: true,
      message: 'Conversion completed!',
      downloadUrl: `/api/download/${path.basename(result)}`,
      file: path.basename(result),
      size: (await fs.stat(result)).size
    });

  } catch (error) {
    console.error('Conversion error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message,
      details: error.stack 
    });
  }
});

// Download endpoint
router.get('/download/:filename', async (req, res) => {
  try {
    const filePath = path.join(__dirname, '../output', req.params.filename);
    
    if (!await fs.pathExists(filePath)) {
      return res.status(404).json({ error: 'File not found' });
    }

    res.download(filePath, (err) => {
      if (err) {
        console.error('Download error:', err);
      }
      // Clean up after download
      setTimeout(() => {
        fs.remove(path.dirname(filePath)).catch(console.error);
      }, 10000);
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Status endpoint
router.get('/status/:jobId', (req, res) => {
  // If using background jobs with Bull/Redis, implement here
  res.json({ status: 'processing', jobId: req.params.jobId });
});

module.exports = router;