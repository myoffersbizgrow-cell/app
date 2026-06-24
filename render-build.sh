#!/usr/bin/env bash
set -o errexit

echo "📦 Setting up Java for Node.js..."

# ✅ Install Java
apt-get update -y
apt-get install -y openjdk-17-jdk-headless

# ✅ Verify Java
java -version

# ✅ Install Node dependencies
npm install

echo "✅ Build completed!"
