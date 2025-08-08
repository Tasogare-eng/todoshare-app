# Railway Deployment Guide

## Prerequisites
- Railway account (https://railway.app)
- GitHub repository pushed (✓ already done)
- Railway CLI installed (optional but recommended)

## Installation of Railway CLI (optional)
```bash
npm install -g @railway/cli
railway login
```

## Deployment Steps

### 1. Create New Railway Project
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `todoshare-app` repository

### 2. Deploy Backend (FastAPI)
1. In Railway dashboard, click "Add Service"
2. Select "GitHub Repo" → your repository
3. Configure the backend service:
   - **Root Directory**: `/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Backend Environment Variables
Add these in Railway service settings:
```
PORT=8000
JWT_SECRET_KEY=your-super-secret-jwt-key-here-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=*
```

### 3. Deploy Frontend (Vue 3)
1. Add another service to the same project
2. Configure the frontend service:
   - **Root Directory**: `/frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview`

#### Frontend Environment Variables
```
VITE_API_BASE_URL=https://your-backend-service-url.railway.app
```

### 4. Alternative: Single Service Deployment

Create a `railway.json` in the root directory:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}
```

### 5. Configure Custom Domains (optional)
1. In Railway dashboard, go to your service
2. Click "Settings" → "Domains"
3. Add custom domain or use provided Railway domain

## Important Configuration Files

### Backend: Add health check endpoint
Add to `/backend/app/main.py`:
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Frontend: Update API base URL
Update `/frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
```

### Backend: Update CORS for production
Update `/backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment Commands (CLI method)
```bash
# Login to Railway
railway login

# Link to existing project
railway link

# Deploy backend
cd backend
railway up

# Deploy frontend  
cd ../frontend
railway up
```

## Post-Deployment Checklist
- [ ] Backend service is running and accessible
- [ ] Frontend service is running and accessible  
- [ ] API calls from frontend to backend are working
- [ ] Authentication flow works end-to-end
- [ ] Environment variables are properly set
- [ ] Custom domains configured (if needed)

## Troubleshooting

### Common Issues:
1. **CORS errors**: Update CORS_ORIGINS environment variable
2. **API connection failed**: Check VITE_API_BASE_URL points to backend service
3. **Build failures**: Ensure all dependencies are in package.json/requirements.txt
4. **Port issues**: Railway automatically sets PORT environment variable

### Useful Railway Commands:
```bash
railway logs        # View service logs
railway status      # Check service status
railway variables   # Manage environment variables
railway open        # Open service in browser
```

## Cost Estimation
- Railway offers $5/month free tier
- Each service uses separate resources
- Monitor usage in Railway dashboard

Your TodoShare app should be accessible at the Railway-provided URLs once deployed!