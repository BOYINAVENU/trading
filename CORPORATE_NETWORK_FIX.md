# 🔒 Corporate Network SSL Fix

## Problem
You're seeing SSL certificate errors when installing packages:
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain
```

This happens when your corporate network uses a proxy that intercepts HTTPS traffic with self-signed certificates.

---

## ✅ Quick Fix (Use Trusted Host)

### Option 1: Install with Trusted Host Flag (RECOMMENDED)

```bash
# Activate virtual environment
venv\Scripts\activate

# Install with trusted host flags
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Option 2: Use setup_corporate.bat Script

I've created a special setup script for corporate networks:

```bash
# Run corporate network setup
setup_corporate.bat
```

---

## 🔧 Permanent Solution

### Configure pip to Always Trust PyPI

Create a `pip.ini` file in your user directory:

**Location**: `C:\Users\AL55582\pip\pip.ini`

**Contents**:
```ini
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
```

**How to create**:
```bash
# Create directory
mkdir C:\Users\AL55582\pip

# Create file
echo [global] > C:\Users\AL55582\pip\pip.ini
echo trusted-host = pypi.python.org >> C:\Users\AL55582\pip\pip.ini
echo                pypi.org >> C:\Users\AL55582\pip\pip.ini
echo                files.pythonhosted.org >> C:\Users\AL55582\pip\pip.ini
```

---

## 🚨 Alternative: Disable SSL Verification (NOT RECOMMENDED)

**⚠️ Only use this if trusted-host doesn't work**

```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --disable-pip-version-check -r requirements.txt
```

---

## 📝 Step-by-Step Fix

### 1. Activate Virtual Environment
```bash
cd C:\Users\AL55582\CascadeProjects\polymarket-sniper
venv\Scripts\activate
```

### 2. Upgrade pip with Trusted Host
```bash
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

### 3. Install Dependencies with Trusted Host
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 4. Verify Installation
```bash
python test_setup.py
```

---

## 🌐 Corporate Proxy Configuration

If your network also requires proxy authentication:

```bash
# Set proxy environment variables
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080

# Then install with trusted host
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

Or create `pip.ini` with proxy:
```ini
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
proxy = http://proxy.company.com:8080
```

---

## 🔍 Troubleshooting

### Error: "Could not fetch URL"
**Solution**: Add all three trusted hosts:
```bash
--trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

### Error: "Proxy authentication required"
**Solution**: Include credentials in proxy URL:
```bash
set HTTP_PROXY=http://username:password@proxy.company.com:8080
```

### Error: Still failing
**Solution**: Contact IT to get corporate CA certificate, then:
```bash
pip install --cert path\to\corporate-cert.pem -r requirements.txt
```

---

## ✅ Success Check

After installation, you should see:
```
Successfully installed py-clob-client-0.20.0 web3-6.0.0 ...
```

Then verify:
```bash
python test_setup.py
```

---

## 🎯 Quick Commands Reference

```bash
# Install everything (corporate network)
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Upgrade pip (corporate network)
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# Install single package (corporate network)
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org package-name
```

---

**Use the setup_corporate.bat script for automatic installation with corporate network support!**
