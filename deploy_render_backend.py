#!/usr/bin/env python3

import json
import urllib.request
import urllib.error
import sys
import os

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
    if owners_data:
        owner = owners_data[0]
        owner_id = owner['id']
        print(f'✓ Owner ID: {owner_id}')
    else:
        print('✗ No owners found')
        sys.exit(1)
except urllib.error.HTTPError as e:
    print(f'✗ HTTP {e.code}: {e.reason}')
    print(e.read().decode('utf-8'))
    sys.exit(1)
except Exception as e:
    print(f'✗ Error: {e}')
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
        'pythonVersion': '3.11',
        'buildCommand': 'pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput',
        'startCommand': 'gunicorn config.wsgi:application --bind 0.0.0.0:10000',
        'healthCheckPath': '/api/schema/'
    },
    'envVars': [
        {'key': 'DEBUG', 'value': 'False'},
        {'key': 'ALLOWED_HOSTS', 'value': '*.render.com,breathing-esg-backend.onrender.com'},
        {'key': 'SECRET_KEY', 'value': 'django-production-secret-key-change-me'},
        {'key': 'DB_ENGINE', 'value': 'django.db.backends.postgresql'},
        {'key': 'DB_NAME', 'value': 'breathe_esg'},
        {'key': 'DB_USER', 'value': 'postgres'},
        {'key': 'DB_PASSWORD', 'value': 'change-me'},
        {'key': 'DB_HOST', 'value': 'localhost'},
        {'key': 'DB_PORT', 'value': '5432'},
        {'key': 'CORS_ALLOWED_ORIGINS', 'value': 'https://breathe-esg-frontend-oa4lv1agf-ankitsingh-webs-projects.vercel.app'}
    ]
}

req_data = json.dumps(service_payload).encode('utf-8')
req = urllib.request.Request('https://api.render.com/v1/services', headers=headers, data=req_data, method='POST')

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        service_resp = json.load(resp)
    print(f"✓ Service created: {service_resp['service']['name']}")
    print(f"  Service ID: {service_resp['service']['id']}")
    print(f"  Dashboard: {service_resp['service']['dashboardUrl']}")
except urllib.error.HTTPError as e:
    error_msg = e.read().decode('utf-8')
    print(f'✗ HTTP {e.code}: {e.reason}')
    print(error_msg)
    # Continue even if service creation fails (it may already exist)
except Exception as e:
    print(f'✗ Error: {e}')
    sys.exit(1)

print('\n✓ Backend deployment initiated on Render!')
print('Note: Render will auto-deploy from the GitHub repository.')
print('You may need to set up PostgreSQL database and configure environment variables in the Render dashboard.')
