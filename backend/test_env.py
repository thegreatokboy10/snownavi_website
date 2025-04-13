#!/usr/bin/env python3
"""
Test script to verify that environment variables are being loaded correctly.
Run this script to check if the .env file is being properly loaded.
"""

import os
import sys
from dotenv import load_dotenv

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the .env file
env_path = os.path.join(script_dir, '.env')

print(f"Looking for .env file at: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")

# Load environment variables from .env file
load_dotenv(env_path)

# Check if environment variables are set
google_client_id = os.environ.get('GOOGLE_CLIENT_ID', 'Not set')
allowed_emails = os.environ.get('ALLOWED_EMAILS', 'Not set')

print("\nEnvironment Variables:")
print(f"GOOGLE_CLIENT_ID: {google_client_id}")
print(f"ALLOWED_EMAILS: {allowed_emails}")

# Check if the variables are properly set
if google_client_id == 'Not set' or allowed_emails == 'Not set':
    print("\n❌ ERROR: One or more required environment variables are not set.")
    sys.exit(1)
else:
    print("\n✅ SUCCESS: All required environment variables are set.")
    sys.exit(0)
