# Breathe ESG - Deployment Guide

## Local Development 

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Access at: http://localhost:5173/

---

## Production Deployment

### Step 1: Push to GitHub

```bash
cd c:\Users\ankit\OneDrive\Desktop\breathe-esg
git add .
git commit -m "Update documentation and project settings"
git push
```

If the repository is not connected yet, add the remote using:

```bash
git remote add origin https://github.com/ankitsingh-web/Breathe-ESG.git
git push -u origin main
```

### Step 2: Deploy Backend on Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Create New Project
4. Select "Deploy from GitHub repo"
5. Connect your breathe-esg repo
6. Railway auto-detects Django
7. Add PostgreSQL database from Railway Marketplace
8. Environment variables auto-configured
9. Deploy!

Backend URL: https://breathe-esg-backend.railway.app

### Step 3: Deploy Frontend on Vercel

1. Go to https://vercel.com
2. Sign up with GitHub
3. Import your breathe-esg repo
4. Framework: Vite
5. Root Directory: `frontend`
6. Build Command: `npm run build`
7. Output: `dist`
8. Add environment variable:
   ```
   VITE_API_BASE_URL=https://breathe-esg-backend.railway.app/api
   ```
9. Deploy!

Frontend URL: https://breathe-esg.vercel.app

---

## API Endpoints

- `POST /api/upload/` - Upload CSV file
- `GET /api/records/` - Get all emission records
- `PATCH /api/approve/<id>/` - Approve a record
- `GET /api/schema/` - Swagger API docs
- `GET /api/redoc/` - ReDoc API docs

---

## Sample CSV Format

```csv
activity_type,value,unit,scope,record_date
Diesel,1000,liters,SCOPE1,2026-01-01
Electricity,25000,kwh,SCOPE2,2026-01-01
Flight,1200,kwh,SCOPE3,2026-01-01
```

---

## Tech Stack

**Backend:**
- Django 5.0.6
- Django REST Framework
- PostgreSQL
- Pandas

**Frontend:**
- React 18
- Vite
- Material UI
- Axios

**Deployment:**
- Railway (Backend + Database)
- Vercel (Frontend)
