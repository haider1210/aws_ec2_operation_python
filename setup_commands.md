

# System Setup and Usage (Linux & Windows)

---

## **Linux Setup**

### 1. System Update & Install Required Packages

```bash
sudo apt update
sudo apt install -y python3-full python3-venv awscli
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install sh
```

### 4. Verify AWS CLI Installation

```bash
aws --version
```

### 5. Example Script Execution

Replace placeholders with your AWS credentials and instance details:

```bash
python ec2_operations.py \
  --key_id YOUR_AWS_ACCESS_KEY_ID \
  --access_key YOUR_AWS_SECRET_ACCESS_KEY \
  --region ap-south-1 \
  --operation stop \
  --instance_id i-0123456789abcdef0
```

### 6. Supported Operations

* `start`
* `stop`
* `reboot`
* `terminate`

### 7. Usage Example

Start multiple instances:

```bash
python ec2_operations.py \
  --key_id YOUR_ACCESS_KEY \
  --access_key YOUR_SECRET_KEY \
  --region ap-south-1 \
  --operation start \
  --instance_id i-012abcdef0 i-987699789abcdef0
```

### Sample Output

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

---

## **Windows Setup (PowerShell)**

### 1. Install Python & AWS CLI

```powershell
# Install Python (if not installed)
winget install Python.Python.3

# Install AWS CLI
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

### 2. Create and Activate Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```powershell
pip install sh
```

### 4. Verify AWS CLI Installation

```powershell
aws --version
```

### 5. Example Script Execution

```powershell
python ec2_operations.py `
  --key_id YOUR_AWS_ACCESS_KEY_ID `
  --access_key YOUR_AWS_SECRET_ACCESS_KEY `
  --region ap-south-1 `
  --operation stop `
  --instance_id i-0123456789abcdef0
```

### 6. Supported Operations

* `start`
* `stop`
* `reboot`
* `terminate`

### 7. Usage Example

```powershell
python ec2_operations.py `
  --key_id YOUR_ACCESS_KEY `
  --access_key YOUR_SECRET_KEY `
  --region ap-south-1 `
  --operation start `
  --instance_id i-012abcdef0 i-987699789abcdef0
```

### Sample Output

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


