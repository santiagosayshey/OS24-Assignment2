#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install pandas matplotlib seaborn

# Create a requirements.txt file
pip freeze > requirements.txt

echo "Virtual environment setup complete. To activate, run: source venv/bin/activate"