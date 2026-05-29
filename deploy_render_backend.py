#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request
import urllib.error
import sys

TOKEN = 'rnd_aRgBV2BdGIcfhMN5JDN2IiRMIYSH'
REPO_URL = 'https://github.com/ankitsingh-web/Breathe-ESG.git'
BACKEND_ROOT_DIR = 'backend'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Step 1: Get workspace/owner ID
print('[Step 1] Fetching Render workspace...')
try:
    req = urllib.request.Request('https://api.render.com/v1/owners', headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        owners_data = json.load(resp)
    
    # API returns: [{"cursor": "...", "owner": {"id": "...", "name": "...", ...}}]
    owner_id = None
    if isinstance(owners_data, list) and len(owners_data) > 0:
        if 'owner' in owners_data[0]:
            owner_id = owners_data[0]['owner'].get('id')
        elif 'id' in owners_data[0]:
            owner_id = owners_data[0]['id']
    
    if owner_id:
        print(f'[OK] Owner ID: {owner_id}')
    else:
        print('[ERROR] Could not extract owner ID from API response')
        print(f'[DEBUG] Response structure: {owners_data}')
        sys.exit(1)
except urllib.error.HTTPError as e:
    print(f'[ERROR] HTTP {e.code}: {e.reason}')
    print(e.read().decode('utf-8'))
    sys.exit(1)
except Exception as e:
    print(f'[ERROR] {type(e).__name__}: {e}')
    sys.exit(1)

# Step 2: Create backend service
print('\n[Step 2] Creating backend service on Render...')
service_payload = {
    'type': 'web_service',
    'name': 'breathe-esg-backend',
    'ownerId': owner_id,
    'repo': REPO_URL,
    'branch': 'main',
    'rootDir': BACKEND_ROOT_DIR,
    'autoDeploy': 'yes',
    'serviceDetails': {
        'env': 'python',
        'envSpecificDetails': {
            'pythonVersion': '3.11',
            'buildCommand': 'pip install -r requirements.txt && python manage.py migrate',
            'startCommand': 'gunicorn config.wsgi:application --bind 0.0.0.0:10000'
        }
    },
    'envVars': [
        {'key': 'DEBUG', 'value': 'False'},
        {'key': 'ALLOWED_HOSTS', 'value': '*.render.com'},
        {'key': 'SECRET_KEY', 'value': 'django-insecure-render-prod-change-me'},
        {'key': 'DB_ENGINE', 'value': 'django.db.backends.sqlite3'},
        {'key': 'DB_NAME', 'value': 'db.sqlite3'}
    ]
}

req_data = json.dumps(service_payload).encode('utf-8')
req = urllib.request.Request('https://api.render.com/v1/services', headers=headers, data=req_data, method='POST')

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        service_resp = json.load(resp)
    service_info = service_resp.get('service', service_resp)
    svc_id = service_info.get('id', 'N/A')
    svc_name = service_info.get('name', 'unknown')
    svc_url = service_info.get('dashboardUrl', 'N/A')
    print(f"[OK] Service created: {svc_name}")
    print(f"  Service ID: {svc_id}")
    print(f"  Dashboard: {svc_url}")
except urllib.error.HTTPError as e:
    error_msg = e.read().decode('utf-8')
    print(f'[ERROR] HTTP {e.code}: {e.reason}')
    print(f'  {error_msg}')
except Exception as e:
    print(f'[ERROR] {type(e).__name__}: {e}')
    sys.exit(1)

print('\n[SUCCESS] Backend deployment initiated on Render!')
print('View and manage your service at: https://dashboard.render.com')

