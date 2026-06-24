#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "📦 Setting up Java + Python for Render..."

# ==================== JAVA SETUP ====================
echo "→ Installing Java 17..."
mkdir -p java
cd java

# Download and extract Java
wget -q https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.12%2B7/OpenJDK17U-jdk_x64_linux_hotspot_17.0.12_7.tar.gz -O jdk.tar.gz

tar -xzf jdk.tar.gz
rm jdk.tar.gz  # cleanup

export JAVA_HOME=$(pwd)/jdk-17.0.12+7
export PATH=$JAVA_HOME/bin:$PATH

cd ..

echo "✅ Java installed:"
java -version

# ==================== ANDROID TOOLS ====================
echo "→ Setting up Android tools..."
if [ -d "tools" ]; then
    echo "✅ tools/ directory found:"
    ls -la tools/
    chmod +x tools/aapt2 2>/dev/null || true
    echo "✅ aapt2 made executable"
else
    echo "⚠️  tools/ directory not found!"
fi

# ==================== PYTHON DEPENDENCIES ====================
echo "→ Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

echo "✅ Build completed successfully!"
