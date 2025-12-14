# AWS EC2 CLI Automation using Python

This project automates AWS EC2 instance operations using Python and the AWS CLI.

## Features
- Start, Stop, Reboot, Terminate EC2 instances
- Monitor instance state until desired state is reached
- Fetch EC2 details (Name, State, Private IP, Public IP)
- Uses AWS CLI via Python (no boto3)

## Prerequisites
- Linux / WSL
- Python 3.10+
- AWS CLI installed
- AWS Access Key & Secret Key

## Installation
```bash
sudo apt update
sudo apt install -y python3-full python3-venv awscli
python3 -m venv venv
source venv/bin/activate
pip install sh
