import os
import subprocess
import sys
import shutil
import zipfile
<<<<<<< HEAD
import json
=======
>>>>>>> origin/main
import urllib.request
import time
import re
from pathlib import Path

class APKtoAABConverter:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.tools_dir = self.base_dir / "tools"
        self.uploads_dir = self.base_dir / "uploads"
        self.output_dir = self.base_dir / "output"
        self.temp_dir = self.base_dir / "temp"
        
<<<<<<< HEAD
        # Keystore path
=======
        # Keystore
>>>>>>> origin/main
        self.keystore = self.base_dir / "release.jks"
        self.keystore_pass = "123456"
        self.key_alias = "key0"
        
        # Create directories
        for dir_path in [self.tools_dir, self.uploads_dir, self.output_dir, self.temp_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Tool paths
        self.apktool = self.tools_dir / "apktool.jar"
<<<<<<< HEAD
        self.aapt2 = self.tools_dir / "aapt2.exe"
=======
        self.aapt2 = self.tools_dir / "aapt2"
>>>>>>> origin/main
        self.bundletool = self.tools_dir / "bundletool.jar"
        self.android_jar = self.tools_dir / "android.jar"
        
        # Java check
        self.java = self._find_java()

    def _find_java(self):
        """Find Java installation"""
<<<<<<< HEAD
        try:
            subprocess.run(["java", "-version"], capture_output=True, check=True)
            print("✅ Java found!")
            return "java"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        import glob
        java_paths = [
            "C:/Program Files/Java/jdk-*/bin/java.exe",
            "C:/Program Files/Java/jre-*/bin/java.exe",
            "C:/Program Files/OpenJDK/openjdk-*/bin/java.exe"
        ]
        
        for pattern in java_paths:
            matches = glob.glob(pattern)
            if matches:
                print(f"✅ Java found at: {matches[0]}")
                return matches[0]
        
        print("❌ Java not found! Please install Java JDK 11 or higher.")
        print("Download from: https://adoptium.net/")
        sys.exit(1)

    def download_tools(self):
        """Download required Android tools"""
=======
        # Check Render's Java path first
        java_paths = [
            "/opt/render/project/src/java/jdk-17.0.12+7/bin/java",
            "/usr/bin/java",
            "java"
        ]
        
        for path in java_paths:
            try:
                subprocess.run([path, "-version"], capture_output=True, check=True)
                print(f"✅ Java found: {path}")
                return path
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print("❌ Java not found!")
        sys.exit(1)

    def download_tools(self):
        """Download required Android tools (if not exists)"""
>>>>>>> origin/main
        print("📦 Downloading Android tools...")
        
        tools = {
            "apktool.jar": "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat",
<<<<<<< HEAD
            "aapt2.exe": "https://dl.google.com/dl/android/maven2/com/android/tools/build/aapt2/7.1.0-7984345/aapt2-7.1.0-7984345-windows.zip",
=======
>>>>>>> origin/main
            "bundletool.jar": "https://github.com/google/bundletool/releases/download/1.16.1/bundletool-all-1.16.1.jar",
            "android.jar": "https://github.com/airwire/android-platforms/raw/main/android-33.jar"
        }
        
        for filename, url in tools.items():
            target_path = self.tools_dir / filename
            if target_path.exists():
                print(f"  ✅ {filename} already exists")
                continue
            
            print(f"  📥 Downloading {filename}...")
            try:
<<<<<<< HEAD
                if filename == "aapt2.exe":
                    zip_path = self.tools_dir / "aapt2.zip"
                    urllib.request.urlretrieve(url, zip_path)
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(self.tools_dir)
                    os.remove(zip_path)
                    aapt2_exe = self.tools_dir / "aapt2.exe"
                    if not aapt2_exe.exists():
                        for f in self.tools_dir.glob("*.exe"):
                            if "aapt2" in f.name.lower():
                                f.rename(aapt2_exe)
                else:
                    urllib.request.urlretrieve(url, target_path)
=======
                urllib.request.urlretrieve(url, target_path)
>>>>>>> origin/main
                print(f"  ✅ Downloaded {filename}")
            except Exception as e:
                print(f"  ❌ Failed to download {filename}: {e}")
        
        print("✅ All tools downloaded!")

<<<<<<< HEAD
    def _delete_if_exists(self, file_path):
        """✅ Auto-delete file if it exists"""
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"  🗑️ Deleted old file: {file_path.name}")
                return True
            except Exception as e:
                print(f"  ⚠️ Could not delete {file_path.name}: {e}")
                # Try alternative name
                new_path = file_path.parent / (file_path.stem + "_new" + file_path.suffix)
                print(f"  📁 Using alternative: {new_path.name}")
                return new_path
        return file_path

    def decompile_apk(self, apk_path, output_dir):
        """Decompile APK using apktool"""
        cmd = [
            self.java, "-jar", str(self.apktool),
            "d", str(apk_path),
            "-o", str(output_dir),
            "-f"
        ]
=======
    def decompile_apk(self, apk_path, output_dir):
        cmd = [self.java, "-jar", str(self.apktool), "d", str(apk_path), "-o", str(output_dir), "-f"]
>>>>>>> origin/main
        print(f"🔧 Decompiling APK...")
        self._run_command(cmd)

    def _extract_dex_from_apk(self, apk_path, output_dir):
<<<<<<< HEAD
        """Extract DEX files directly from APK"""
        print("🔧 Extracting DEX files from APK...")
=======
        print("🔧 Extracting DEX files...")
>>>>>>> origin/main
        dex_count = 0
        with zipfile.ZipFile(apk_path, 'r') as apk_zip:
            for file_name in apk_zip.namelist():
                if file_name.endswith('.dex'):
                    apk_zip.extract(file_name, output_dir)
                    dex_count += 1
                    print(f"  ✅ Extracted {file_name}")
<<<<<<< HEAD
        
        if dex_count == 0:
            print("  ⚠️ No DEX files found in APK!")
        else:
            print(f"  ✅ Extracted {dex_count} DEX file(s)")
        return dex_count

    def _fix_public_xml(self, public_xml_path):
        """Remove problematic lines with $ from public.xml"""
        print("🔧 Fixing public.xml...")
        with open(public_xml_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        filtered_lines = [line for line in lines if not ('<public' in line and '$' in line)]
        
=======
        print(f"  ✅ Extracted {dex_count} DEX file(s)")
        return dex_count

    def _fix_public_xml(self, public_xml_path):
        print("🔧 Fixing public.xml...")
        with open(public_xml_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        filtered_lines = [line for line in lines if not ('<public' in line and '$' in line)]
>>>>>>> origin/main
        with open(public_xml_path, 'w', encoding='utf-8') as f:
            f.writelines(filtered_lines)
        print("✅ public.xml fixed")

    def _fix_manifest(self, manifest_path):
<<<<<<< HEAD
        """Remove problematic elements from AndroidManifest.xml"""
        print("🔧 Fixing AndroidManifest.xml...")
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(r'<queries>.*?</queries>', '', content, flags=re.DOTALL)
        content = re.sub(r'<property[^>]*/>', '', content)
        content = re.sub(r'<property[^>]*>.*?</property>', '', content, flags=re.DOTALL)
        
        if 'android:hasCode' not in content:
            content = re.sub(r'<application', '<application android:hasCode="true"', content)
        
        content = '\n'.join(line for line in content.split('\n') if line.strip())
        
=======
        print("🔧 Fixing AndroidManifest.xml...")
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = re.sub(r'<queries>.*?</queries>', '', content, flags=re.DOTALL)
        content = re.sub(r'<property[^>]*/>', '', content)
        if 'android:hasCode' not in content:
            content = re.sub(r'<application', '<application android:hasCode="true"', content)
        content = '\n'.join(line for line in content.split('\n') if line.strip())
>>>>>>> origin/main
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ AndroidManifest.xml fixed")

    def compile_resources(self, decompile_dir, output_zip):
<<<<<<< HEAD
        """Compile resources using aapt2"""
        res_dir = decompile_dir / "res"
        
=======
        res_dir = decompile_dir / "res"
>>>>>>> origin/main
        public_xml = decompile_dir / "res" / "values" / "public.xml"
        if public_xml.exists():
            self._fix_public_xml(public_xml)
        
<<<<<<< HEAD
        cmd = [
            str(self.aapt2), "compile",
            "--dir", str(res_dir),
            "-o", str(output_zip)
        ]
=======
        cmd = [str(self.aapt2), "compile", "--dir", str(res_dir), "-o", str(output_zip)]
>>>>>>> origin/main
        print(f"🔧 Compiling resources...")
        self._run_command(cmd)

    def _restructure_zip(self, input_zip, output_zip, decompile_dir):
<<<<<<< HEAD
        """Restructure zip for bundletool - DEX files in dex/ folder"""
        print("🔧 Restructuring base.zip for bundletool...")
        
=======
        print("🔧 Restructuring zip...")
>>>>>>> origin/main
        extract_dir = input_zip.parent / "extracted"
        extract_dir.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(input_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            manifest_src = extract_dir / "AndroidManifest.xml"
            if manifest_src.exists():
                new_zip.write(manifest_src, "manifest/AndroidManifest.xml")
<<<<<<< HEAD
                print(f"  ✅ Added manifest/AndroidManifest.xml")
=======
>>>>>>> origin/main
            
            res_src = extract_dir / "res"
            if res_src.exists():
                for file_path in res_src.rglob('*'):
                    if file_path.is_file():
                        new_zip.write(file_path, str(file_path.relative_to(extract_dir)))
<<<<<<< HEAD
                print(f"  ✅ Added res/ folder")
=======
>>>>>>> origin/main
            
            resources_pb = extract_dir / "resources.pb"
            if resources_pb.exists():
                new_zip.write(resources_pb, "resources.pb")
<<<<<<< HEAD
                print(f"  ✅ Added resources.pb")
            
            dex_count = 0
            for dex_file in decompile_dir.glob("*.dex"):
                new_zip.write(dex_file, f"dex/{dex_file.name}")
                dex_count += 1
                print(f"  ✅ Added dex/{dex_file.name}")
            
            if dex_count == 0:
                print("  ⚠️ No DEX files found!")
=======
            
            for dex_file in decompile_dir.glob("*.dex"):
                new_zip.write(dex_file, f"dex/{dex_file.name}")
                print(f"  ✅ Added dex/{dex_file.name}")
>>>>>>> origin/main
        
        shutil.rmtree(extract_dir)
        print("✅ Restructured zip created")

    def link_resources(self, decompile_dir, res_zip, output_zip, min_sdk=21, target_sdk=33):
<<<<<<< HEAD
        """Link resources using aapt2"""
=======
>>>>>>> origin/main
        manifest = decompile_dir / "AndroidManifest.xml"
        self._fix_manifest(manifest)
        
        temp_zip = output_zip.parent / "temp_base.zip"
        
        cmd = [
<<<<<<< HEAD
            str(self.aapt2), "link",
            "--proto-format",
            "-o", str(temp_zip),
            "-I", str(self.android_jar),
            "--manifest", str(manifest),
            f"--min-sdk-version", str(min_sdk),
            f"--target-sdk-version", str(target_sdk),
            "--version-code", "1",
            "--version-name", "1.0",
            "-R", str(res_zip),
            "--auto-add-overlay"
=======
            str(self.aapt2), "link", "--proto-format", "-o", str(temp_zip),
            "-I", str(self.android_jar), "--manifest", str(manifest),
            f"--min-sdk-version", str(min_sdk),
            f"--target-sdk-version", str(target_sdk),
            "--version-code", "1", "--version-name", "1.0",
            "-R", str(res_zip), "--auto-add-overlay"
>>>>>>> origin/main
        ]
        
        print(f"🔧 Linking resources...")
        self._run_command(cmd)
<<<<<<< HEAD
        
=======
>>>>>>> origin/main
        self._restructure_zip(temp_zip, output_zip, decompile_dir)
        temp_zip.unlink()

    def build_aab(self, base_zip, output_aab):
<<<<<<< HEAD
        """✅ Build AAB with auto-delete"""
        # ✅ Auto-delete if exists
        output_aab = self._delete_if_exists(output_aab)
        
        cmd = [
            self.java, "-jar", str(self.bundletool),
            "build-bundle",
            "--modules=" + str(base_zip),
            "--output=" + str(output_aab)
        ]
=======
        cmd = [self.java, "-jar", str(self.bundletool), "build-bundle", "--modules=" + str(base_zip), "--output=" + str(output_aab)]
>>>>>>> origin/main
        print(f"🔧 Building AAB...")
        self._run_command(cmd)
        return output_aab

    def build_apks_from_aab(self, aab_path):
<<<<<<< HEAD
        """✅ Generate APKs with auto-delete"""
        print("\n🔧 Generating APKs from AAB...")
        
        apks_output = self.output_dir / "app-universal.apks"
        
        # ✅ Auto-delete if exists
        apks_output = self._delete_if_exists(apks_output)
        
        # Use keystore for signing
        cmd = [
            self.java, "-jar", str(self.bundletool),
            "build-apks",
            "--bundle=" + str(aab_path),
            "--output=" + str(apks_output),
            "--mode=universal",
            "--ks=" + str(self.keystore),
            "--ks-pass=pass:" + self.keystore_pass,
            "--ks-key-alias=" + self.key_alias
        ]
        
        print(f"  Using keystore: {self.keystore}")
        print(f"  Key alias: {self.key_alias}")
=======
        print("\n🔧 Generating APKs from AAB...")
        apks_output = self.output_dir / "app-universal.apks"
        
        # Use keystore
        cmd = [
            self.java, "-jar", str(self.bundletool),
            "build-apks", "--bundle=" + str(aab_path),
            "--output=" + str(apks_output),
            "--mode=universal"
        ]
        
        if self.keystore.exists():
            cmd.extend(["--ks=" + str(self.keystore), "--ks-pass=pass:" + self.keystore_pass, "--ks-key-alias=" + self.key_alias])
            print(f"  Using keystore: {self.keystore}")
        else:
            print("  Using debug keystore")
>>>>>>> origin/main
        
        self._run_command(cmd)
        
        # Extract universal APK
        extract_dir = self.output_dir / "universal"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        extract_dir.mkdir(exist_ok=True)
        
<<<<<<< HEAD
        print("🔧 Extracting universal APK...")
=======
>>>>>>> origin/main
        with zipfile.ZipFile(apks_output, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        universal_apk = extract_dir / "universal.apk"
        if universal_apk.exists():
            print(f"✅ Universal APK created: {universal_apk}")
            return universal_apk
<<<<<<< HEAD
        else:
            print("⚠️ Universal APK not found!")
            return None

    def _run_command(self, cmd):
        """Run a command and handle errors"""
        cmd_str = " ".join(str(c) for c in cmd)
        print(f"  Running: {cmd_str}")
        
=======
        return None

    def _run_command(self, cmd):
        """Run command with proper PATH"""
        cmd_str = " ".join(str(c) for c in cmd)
        print(f"  Running: {cmd_str}")
        
        env = os.environ.copy()
        java_dir = Path(self.java).parent
        env["PATH"] = f"{java_dir}:{env.get('PATH', '')}"
        
>>>>>>> origin/main
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
<<<<<<< HEAD
                timeout=600
            )
            
            if result.returncode != 0:
                print(f"❌ Command failed!")
                print(f"STDERR: {result.stderr}")
                raise Exception(f"Command failed: {result.stderr}")
            
            if result.stdout:
                print(f"  Output: {result.stdout[:200]}...")
            return result
        except subprocess.TimeoutExpired:
            raise Exception("Command timed out after 10 minutes")
        except Exception as e:
            raise Exception(f"Command failed: {e}")

    def convert(self, apk_filename, min_sdk=21, target_sdk=33):
        """Main conversion process"""
        apk_path = self.uploads_dir / apk_filename
        
=======
                timeout=600,
                env=env
            )
            if result.returncode != 0:
                raise Exception(result.stderr)
            if result.stdout:
                print(f"  Output: {result.stdout[:200]}...")
            return result
        except Exception as e:
            raise Exception(f"Command failed: {e}")

    def convert(self, apk_path, min_sdk=21, target_sdk=33):
        """Main conversion"""
        apk_path = Path(apk_path)
>>>>>>> origin/main
        if not apk_path.exists():
            print(f"❌ APK not found: {apk_path}")
            return None
        
<<<<<<< HEAD
        # Check keystore
        if not self.keystore.exists():
            print(f"⚠️ Keystore not found: {self.keystore}")
            print("  APKs will be signed with debug keystore")
            use_debug = True
        else:
            print(f"✅ Keystore found: {self.keystore}")
            use_debug = False
        
        print(f"\n🚀 Starting conversion for: {apk_filename}")
=======
        print(f"\n🚀 Starting conversion for: {apk_path.name}")
>>>>>>> origin/main
        print(f"  Min SDK: {min_sdk}, Target SDK: {target_sdk}")
        
        job_id = str(int(time.time()))
        job_dir = self.temp_dir / job_id
        job_dir.mkdir(exist_ok=True)
        
        try:
<<<<<<< HEAD
            # 1. Decompile APK
            decompile_dir = job_dir / "decompiled"
            self.decompile_apk(apk_path, decompile_dir)
            
            # 2. Extract DEX files
            dex_dir = job_dir / "dex"
            dex_dir.mkdir(exist_ok=True)
            self._extract_dex_from_apk(apk_path, dex_dir)
            
            for dex_file in dex_dir.glob("*.dex"):
                shutil.copy(dex_file, decompile_dir / dex_file.name)
                print(f"  ✅ Copied {dex_file.name} to decompiled folder")
            
            # 3. Compile resources
            res_zip = job_dir / "res.zip"
            self.compile_resources(decompile_dir, res_zip)
            
            # 4. Link resources
            base_zip = job_dir / "base.zip"
            self.link_resources(decompile_dir, res_zip, base_zip, min_sdk, target_sdk)
            
            # 5. Build AAB (auto-delete old)
            output_filename = apk_path.stem + ".aab"
            output_aab = self.output_dir / output_filename
            output_aab = self.build_aab(base_zip, output_aab)
            
            print(f"\n✅ AAB created: {output_aab}")
            
            # 6. Generate APKs (auto-delete old)
=======
            decompile_dir = job_dir / "decompiled"
            self.decompile_apk(apk_path, decompile_dir)
            
            dex_dir = job_dir / "dex"
            dex_dir.mkdir(exist_ok=True)
            self._extract_dex_from_apk(apk_path, dex_dir)
            for dex_file in dex_dir.glob("*.dex"):
                shutil.copy(dex_file, decompile_dir / dex_file.name)
            
            res_zip = job_dir / "res.zip"
            self.compile_resources(decompile_dir, res_zip)
            
            base_zip = job_dir / "base.zip"
            self.link_resources(decompile_dir, res_zip, base_zip, min_sdk, target_sdk)
            
            output_filename = apk_path.stem + ".aab"
            output_aab = self.output_dir / output_filename
            self.build_aab(base_zip, output_aab)
            
            print(f"\n✅ AAB created: {output_aab}")
            
>>>>>>> origin/main
            universal_apk = self.build_apks_from_aab(output_aab)
            
            print(f"\n✅ Conversion complete!")
            print(f"📁 AAB: {output_aab}")
<<<<<<< HEAD
            if universal_apk and universal_apk.exists():
                print(f"📱 APK: {universal_apk}")
            
            # Clean up
            shutil.rmtree(job_dir)
            
=======
            if universal_apk:
                print(f"📱 APK: {universal_apk}")
            
            shutil.rmtree(job_dir)
>>>>>>> origin/main
            return output_aab
            
        except Exception as e:
            print(f"\n❌ Conversion failed: {e}")
            if job_dir.exists():
                shutil.rmtree(job_dir)
            return None
<<<<<<< HEAD

    def interactive_mode(self):
        """Interactive mode for easy use"""
        print("\n" + "="*50)
        print("📱 APK to AAB Converter (Python)")
        print("="*50)
        
        # Check keystore
        if self.keystore.exists():
            print(f"✅ Keystore found: {self.keystore}")
        else:
            print(f"⚠️ Keystore not found: {self.keystore}")
            print("  APKs will use debug keystore")
        
        # Check tools
        if not self.apktool.exists() or not self.aapt2.exists():
            self.download_tools()
        
        # List APK files
        apk_files = list(self.uploads_dir.glob("*.apk"))
        
        if not apk_files:
            print(f"\n❌ No APK files found in: {self.uploads_dir}")
            print("Please copy your APK file to the 'uploads' folder.")
            return
        
        print("\n📂 Available APK files:")
        for i, apk in enumerate(apk_files, 1):
            size_mb = apk.stat().st_size / (1024 * 1024)
            print(f"  {i}. {apk.name} ({size_mb:.2f} MB)")
        
        choice = input("\nSelect APK number (or 'q' to quit): ")
        if choice.lower() == 'q':
            return
        
        try:
            idx = int(choice) - 1
            apk_path = apk_files[idx]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
        
        min_sdk = input("Min SDK (default: 21): ") or "21"
        target_sdk = input("Target SDK (default: 33): ") or "33"
        
        self.convert(apk_path.name, int(min_sdk), int(target_sdk))

def main():
    converter = APKtoAABConverter()
    converter.interactive_mode()

if __name__ == "__main__":
    main()
=======
>>>>>>> origin/main
