# Frontend-Backend Connection Setup

## Development Mode (Local Testing)

Your frontend is configured to automatically connect to the local backend at `http://localhost:8000/api`.

**To test locally:**

1. **Start the Django backend:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Start the React frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the app:**
   - Open http://localhost:5173 in your browser
   - The frontend will connect to http://localhost:8000/api automatically

---

## Production Mode (After Backend Deployment)

Once your backend is deployed on Render:

1. **Update `frontend/.env.production`:**
   ```
   VITE_API_BASE_URL=https://YOUR-RENDER-BACKEND-URL/api
   ```

2. **The frontend on Vercel will automatically use this URL**

### Getting Your Render Backend URL

After you deploy to Render (requires adding payment info):

1. Go to https://dashboard.render.com
2. Find your `breathe-esg-backend` service
3. Copy the service URL (e.g., `https://breathe-esg-backend-xxxxx.onrender.com`)
4. Update `frontend/.env.production` with: `https://YOUR-SERVICE-URL/api`

---

## Testing the Connection

### In Development

Once both servers are running, test the API:

```bash
# From frontend directory
curl http://localhost:8000/api/
```

Or navigate to: http://localhost:8000/api/docs/ to see Swagger documentation

### In Production

Once deployed, test:

```bash
curl https://YOUR-RENDER-BACKEND-URL/api/
```

---

## Current Status

- **Frontend:** ✅ Live at https://breathe-esg-frontend-oa4lv1agf-ankitsingh-webs-projects.vercel.app
- **Backend:** ⏳ Awaiting Render payment setup
- **API Connection:** ✅ Configured for both local and production environments

## Next Steps

1. Add payment method to Render: https://dashboard.render.com/billing
2. Deploy backend via Render dashboard (see DEPLOYMENT.md)
3. Update `frontend/.env.production` with the actual backend URL
4. Frontend will auto-redeploy and connect to your backend
