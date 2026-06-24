const fs = require('fs-extra');
const path = require('path');
const archiver = require('archiver');

async function createZip(sourceDir, outputPath) {
  return new Promise((resolve, reject) => {
    const output = fs.createWriteStream(outputPath);
    const archive = archiver('zip', { zlib: { level: 9 } });

    output.on('close', resolve);
    archive.on('error', reject);

    archive.pipe(output);
    archive.directory(sourceDir, false);
    archive.finalize();
  });
}

async function extractZip(zipPath, outputDir) {
  const AdmZip = require('adm-zip');
  const zip = new AdmZip(zipPath);
  await fs.ensureDir(outputDir);
  zip.extractAllTo(outputDir, true);
}

async function getFileSize(filePath) {
  const stat = await fs.stat(filePath);
  return stat.size;
}

async function ensureDirectories(dirs) {
  for (const dir of dirs) {
    await fs.ensureDir(dir);
  }
}

module.exports = {
  createZip,
  extractZip,
  getFileSize,
  ensureDirectories
};