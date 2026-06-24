const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);
const fs = require('fs-extra');
const path = require('path');
const AdmZip = require('adm-zip');
const archiver = require('archiver');
const rimraf = require('rimraf');

class APKConverter {
  constructor() {
    this.toolsPath = path.join(__dirname, '../tools');
    this.tempPath = path.join(__dirname, '../temp');
    this.java = 'java';
    this.javaHome = process.env.JAVA_HOME || 'java';
  }

  async convert(apkPath, outputDir, options) {
    const { minSdk, targetSdk, buildTools } = options;
    const jobId = path.basename(outputDir);
    const workDir = path.join(this.tempPath, jobId);

    try {
      // 1. Create working directories
      await fs.ensureDir(workDir);
      await fs.ensureDir(outputDir);
      
      console.log(`Working directory: ${workDir}`);

      // 2. Decompile APK
      const decompileDir = path.join(workDir, 'decompiled');
      await this.decompileApk(apkPath, decompileDir);

      // 3. Compile resources
      const resZip = path.join(workDir, 'res.zip');
      await this.compileResources(decompileDir, resZip);

      // 4. Link resources
      const baseZip = path.join(workDir, 'base.zip');
      await this.linkResources(decompileDir, resZip, baseZip, {
        minSdk,
        targetSdk,
        buildTools
      });

      // 5. Build AAB
      const aabPath = path.join(outputDir, `${path.basename(apkPath, '.apk')}.aab`);
      await this.buildAab(baseZip, aabPath);

      // 6. Clean up temporary files
      await rimraf.sync(workDir);

      console.log(`Conversion complete: ${aabPath}`);
      return aabPath;

    } catch (error) {
      // Clean up on error
      await rimraf.sync(workDir).catch(() => {});
      throw error;
    }
  }

  async decompileApk(apkPath, outputDir) {
    const cmd = `${this.java} -jar ${this.getToolPath('apktool.jar')} d ${apkPath} -o ${outputDir} -f -s`;
    console.log('Decompiling APK...');
    await this.execWithTimeout(cmd, 60000);
    console.log('APK decompiled successfully');
  }

  async compileResources(decompileDir, outputZip) {
    const resDir = path.join(decompileDir, 'res');
    const cmd = `${this.getToolPath('aapt2.exe')} compile --dir ${resDir} -o ${outputZip}`;
    console.log('Compiling resources...');
    await this.execWithTimeout(cmd, 30000);
    console.log('Resources compiled successfully');
  }

  async linkResources(decompileDir, resZip, outputZip, options) {
    const { minSdk, targetSdk } = options;
    const manifest = path.join(decompileDir, 'AndroidManifest.xml');
    const androidJar = this.getToolPath('android.jar');

    // Try to fix public.xml issues
    const publicXml = path.join(decompileDir, 'res', 'values', 'public.xml');
    if (await fs.pathExists(publicXml)) {
      await this.fixPublicXml(publicXml);
    }

    const cmd = `${this.getToolPath('aapt2.exe')} link --proto-format -o ${outputZip} ` +
                `-I ${androidJar} --manifest ${manifest} ` +
                `--min-sdk-version ${minSdk} --target-sdk-version ${targetSdk} ` +
                `--version-code 1 --version-name 1.0 -R ${resZip} --auto-add-overlay`;

    console.log('Linking resources...');
    try {
      await this.execWithTimeout(cmd, 30000);
      console.log('Resources linked successfully');
    } catch (error) {
      console.warn('Link failed, trying with --legacy flag...');
      const legacyCmd = `${this.getToolPath('aapt2.exe')} link --legacy -o ${outputZip} ` +
                        `-I ${androidJar} --manifest ${manifest} ` +
                        `--min-sdk-version ${minSdk} --target-sdk-version ${targetSdk} ` +
                        `--version-code 1 --version-name 1.0 -R ${resZip} --auto-add-overlay`;
      await this.execWithTimeout(legacyCmd, 30000);
    }
  }

  async buildAab(baseZip, outputAab) {
    const cmd = `${this.java} -jar ${this.getToolPath('bundletool.jar')} build-bundle --modules=${baseZip} --output=${outputAab}`;
    console.log('Building AAB...');
    await this.execWithTimeout(cmd, 60000);
    console.log('AAB built successfully');
  }

  async fixPublicXml(publicXmlPath) {
    console.log('Fixing public.xml issues...');
    let content = await fs.readFile(publicXmlPath, 'utf8');
    
    // Remove lines with $ in resource names
    const lines = content.split('\n');
    const filtered = lines.filter(line => !line.includes('$'));
    content = filtered.join('\n');
    
    await fs.writeFile(publicXmlPath, content, 'utf8');
    console.log('public.xml fixed');
  }

  getToolPath(toolName) {
    return path.join(this.toolsPath, toolName).replace(/\\/g, '/');
  }

  async execWithTimeout(cmd, timeout) {
    return new Promise((resolve, reject) => {
      const child = exec(cmd, { 
        maxBuffer: 50 * 1024 * 1024, // 50MB buffer
        timeout: timeout,
        windowsHide: true
      }, (error, stdout, stderr) => {
        if (error) {
          console.error('STDERR:', stderr);
          reject(new Error(`Command failed: ${error.message}\n${stderr}`));
        } else {
          resolve({ stdout, stderr });
        }
      });
    });
  }
}

module.exports = APKConverter;