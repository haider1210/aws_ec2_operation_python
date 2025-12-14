
# AWS EC2 CLI Automation using Python

This project automates **AWS EC2 instance operations** using Python and the AWS CLI, without requiring `boto3`.

---

## Features

* Start, Stop, Reboot, Terminate EC2 instances
* Monitor instance state until the desired state is reached
* Fetch EC2 details: Name, State, Private IP, Public IP
* Uses AWS CLI via Python

---

## Prerequisites

* **Linux / WSL** or **Windows (PowerShell / CMD)**
* Python 3.10+
* AWS CLI installed
* AWS Access Key & Secret Key

---

## Linux Setup

### 1. Install Required Packages

```bash
sudo apt update
sudo apt install -y python3-full python3-venv awscli
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install sh
```

---

## Windows Setup

### 1. Install Python & AWS CLI

```powershell
# Install Python if not already installed
winget install Python.Python.3

# Install AWS CLI
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

### 2. Create & Activate Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```powershell
pip install sh
```

---

## Usage Example

### Linux

```bash
python ec2_operations.py \
  --key_id YOUR_ACCESS_KEY \
  --access_key YOUR_SECRET_KEY \
  --region ap-south-1 \
  --operation start \
  --instance_id i-0123456789abcdef0
```

### Windows

```powershell
python ec2_operations.py `
  --key_id YOUR_ACCESS_KEY `
  --access_key YOUR_SECRET_KEY `
  --region ap-south-1 `
  --operation start `
  --instance_id i-0123456789abcdef0
```

---

## Sample Output

```json
[
    {
        "InstanceId": "i-0123456789abcdef0",
        "Name": "web-server",
        "State": "running",
        "Private IP": "10.0.1.15",
        "Public IP": "13.232.45.10"
    }
]
```
