# Vercel Deployment Guide

## Prerequisites
- Vercel account (https://vercel.com)
- GitHub repository pushed (✓ already done)
- Vercel CLI installed (optional)

## Installation of Vercel CLI (optional)
```bash
npm install -g vercel
vercel login
```

## Deployment Overview
Vercel is optimized for frontend deployments. For full-stack deployment:
- **Frontend**: Deploy directly on Vercel
- **Backend**: Use Vercel Functions (serverless) or external service

## Option 1: Frontend Only Deployment

### 1. Configure Frontend for Production
Create `/frontend/vercel.json`:
```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 2. Deploy Frontend to Vercel
1. Go to https://vercel.com/dashboard
2. Click "New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3. Environment Variables
Add in Vercel project settings:
```
VITE_API_BASE_URL=https://your-backend-url.com
```

## Option 2: Full-Stack with Vercel Functions

### 1. Restructure for Vercel Functions
Create `/api` directory in root:
```
/
├── api/
│   ├── auth/
│   │   ├── login.py
│   │   └── register.py
│   ├── todos/
│   │   ├── index.py
│   │   └── [id].py
│   └── requirements.txt
├── frontend/
└── vercel.json
```

### 2. Create Root `vercel.json`
```json
{
  "framework": "vite",
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.9"
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/$1"
    },
    {
      "source": "/(.*)",
      "destination": "/frontend/dist/$1"
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, POST, PUT, DELETE, OPTIONS"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "Content-Type, Authorization"
        }
      ]
    }
  ]
}
```

### 3. Convert Backend to Serverless Functions

#### `/api/auth/login.py`
```python
from http.server import BaseHTTPRequestHandler
import json
import jwt
import bcrypt
from datetime import datetime, timedelta
import os

# Mock users storage
mock_users = []

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        
        email = data.get('email')
        password = data.get('password')
        
        # Find user
        user = next((u for u in mock_users if u['email'] == email), None)
        
        if not user or not bcrypt.checkpw(password.encode(), user['password'].encode()):
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid credentials'}).encode())
            return
            
        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, os.getenv('JWT_SECRET_KEY', 'secret'), algorithm='HS256')
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'access_token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
```

#### `/api/requirements.txt`
```
PyJWT==2.8.0
bcrypt==4.0.1
```

## Option 3: Hybrid Approach (Recommended)

### Frontend on Vercel + Backend elsewhere
1. **Frontend**: Deploy on Vercel (fast CDN, automatic deployments)
2. **Backend**: Deploy on Railway, Render, or other platform

#### Steps:
1. Deploy frontend to Vercel (Option 1 above)
2. Deploy backend to Railway/Render
3. Update `VITE_API_BASE_URL` to point to backend service

## Deployment Commands (CLI)

### Frontend only:
```bash
cd frontend
vercel --prod
```

### Full project:
```bash
vercel --prod
```

## Configuration Files

### Update `/frontend/vite.config.ts`:
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  base: '/',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000
  }
})
```

### Update API service in frontend:
```typescript
// /frontend/src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// Use relative URLs for Vercel Functions
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

## Environment Variables
Add in Vercel dashboard:
```
JWT_SECRET_KEY=your-super-secret-jwt-key
VITE_API_BASE_URL=https://your-backend-service.com
```

## Pros and Cons

### Vercel Advantages:
- ✅ Excellent for frontend/SPA
- ✅ Automatic deployments from Git
- ✅ Global CDN
- ✅ Great performance
- ✅ Generous free tier

### Vercel Limitations:
- ❌ Serverless functions have cold starts
- ❌ Complex backend logic challenging
- ❌ Database connections limited
- ❌ Function execution time limits

## Recommended Approach
1. **Development**: Use Vercel for frontend + Railway for backend
2. **Production**: Consider dedicated backend hosting for better performance

## Post-Deployment
- Frontend URL: `https://your-project.vercel.app`
- Test all functionality
- Monitor function usage and performance
- Set up custom domain if needed

Choose the option that best fits your needs!