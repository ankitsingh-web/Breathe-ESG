# Breathe ESG Platform

ESG (Environmental, Social, and Governance) emission ingestion and review platform built with Django and React.

## Features

- **CSV Upload**: Upload emissions data from SAP, Utility, and Travel sources
- **Automatic Processing**: Unit normalization, emission calculation, anomaly detection
- **Audit Trail**: Track all changes with django-simple-history
- **Dashboard**: View and approve emission records
- **API Documentation**: Swagger/OpenAPI docs included
- **Multi-tenant**: Support for multiple organizations

## Tech Stack

### Backend
- Django 5.0.6
- Django REST Framework
- PostgreSQL
- Pandas
- Gunicorn

### Frontend
- React 18
- Vite
- Material UI
- Axios
- React Router

## Quick Start

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173/ in your browser.

### Environment Variables

Create `.env` in `backend/`:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

## API Endpoints

- `POST /api/upload/` - Upload CSV file
- `GET /api/records/` - List emission records
- `PATCH /api/approve/<id>/` - Approve a record
- `GET /api/schema/` - OpenAPI schema
- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc

## Sample CSV Format

Supported columns:
- `activity_type`: Diesel, Electricity, Flight, Hotel, etc.
- `value`: Numeric value
- `unit`: liters, gallons, kwh, mwh
- `scope`: SCOPE1, SCOPE2, SCOPE3
- `record_date`: YYYY-MM-DD format

Example:
```csv
activity_type,value,unit,scope,record_date
Diesel,1000,liters,SCOPE1,2026-01-01
Electricity,25000,kwh,SCOPE2,2026-01-01
Flight,1200,kwh,SCOPE3,2026-01-01
```

## Emission Factors

- Diesel: 2.68 kg CO2e per unit
- Electricity: 0.82 kg CO2e per kWh
- Flight: 0.25 kg CO2e per unit
- Hotel: 15 kg CO2e per night

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for full deployment instructions.

Quick deployment:
1. Push to GitHub
2. Deploy backend on Railway (auto-detects Django)
3. Deploy frontend on Vercel

## Project Structure

```
breathe-esg/
├── backend/
│   ├── config/
│   ├── ingestion/
│   ├── emissions/
│   ├── audits/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── README.md
├── DEPLOYMENT.md
└── .gitignore
```

## Key Features Explained

### Unit Normalization
All units are converted to canonical units before emission calculation:
- liters → liters (1:1)
- gallons → liters (×3.78541)
- mwh → kwh (×1000)

### Anomaly Detection
Records with normalized values > 100,000 are flagged as anomalies.

### Audit Trail
All changes to EmissionRecord are tracked in HistoricalEmissionRecord.

## Admin Panel

Access Django admin at `/admin/` with superuser credentials.

## License

MIT

## Support

For issues or questions, contact the development team.
