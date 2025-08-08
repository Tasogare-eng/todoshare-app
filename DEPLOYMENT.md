# TodoShare Deployment Guide

This guide covers deploying TodoShare to production using Vercel (frontend) and Railway (backend).

## Prerequisites

- Git repository hosted on GitHub
- Vercel account
- Railway account
- Domain name (optional)

## Backend Deployment (Railway)

### 1. Prepare Railway Configuration

The project includes `railway.json` for automatic configuration.

### 2. Deploy to Railway

1. **Sign up/Login to Railway**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   railway login
   ```

2. **Create New Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your TodoShare repository
   - Select the `backend` folder

3. **Set Environment Variables**
   
   In Railway dashboard, add these variables:
   ```env
   # JWT Configuration
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Database (if using Supabase)
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-supabase-anon-key

   # CORS Configuration
   ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000

   # Port (Railway sets this automatically)
   PORT=8000
   ```

4. **Deploy**
   - Railway will automatically build and deploy your backend
   - Get your deployment URL (e.g., `https://your-app.railway.app`)

### 3. Verify Backend Deployment

Test your API endpoints:
```bash
# Health check
curl https://your-app.railway.app/health

# API documentation
curl https://your-app.railway.app/docs
```

## Frontend Deployment (Vercel)

### 1. Prepare Environment Variables

Create `.env.production` in the frontend directory:
```env
VITE_API_BASE_URL=https://your-backend-url.railway.app/api
VITE_APP_TITLE=TodoShare
VITE_APP_VERSION=1.0.0
```

### 2. Deploy to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   vercel login
   ```

2. **Deploy from Local**
   ```bash
   cd frontend
   vercel --prod
   ```

   Or deploy via GitHub:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the `frontend` folder
   - Configure build settings:
     - Build Command: `npm run build`
     - Output Directory: `dist`
     - Install Command: `npm ci`

3. **Set Environment Variables**
   
   In Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Add your production environment variables

4. **Configure Domain** (Optional)
   - Go to Project Settings → Domains
   - Add your custom domain
   - Update DNS records as instructed

## Database Setup (Supabase)

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get your project URL and anon key

### 2. Database Schema

Execute these SQL commands in Supabase SQL Editor:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (if not using Supabase Auth)
CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Categories table
CREATE TABLE categories (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(30) NOT NULL,
    color VARCHAR(7) DEFAULT '#007bff',
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, name)
);

-- Todos table
CREATE TABLE todos (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    priority VARCHAR(10) CHECK (priority IN ('low', 'medium', 'high')),
    due_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Todo categories junction table (many-to-many)
CREATE TABLE todo_categories (
    todo_id UUID REFERENCES todos(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (todo_id, category_id)
);

-- Indexes for performance
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_status ON todos(status);
CREATE INDEX idx_todos_due_date ON todos(due_date);
CREATE INDEX idx_categories_user_id ON categories(user_id);

-- Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE todo_categories ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can only see their own data" ON users
    FOR ALL USING (id = auth.uid());

CREATE POLICY "Users can only see their own todos" ON todos
    FOR ALL USING (user_id = auth.uid());

CREATE POLICY "Users can only see their own categories" ON categories
    FOR ALL USING (user_id = auth.uid());

CREATE POLICY "Users can only see their own todo categories" ON todo_categories
    FOR ALL USING (
        todo_id IN (SELECT id FROM todos WHERE user_id = auth.uid())
    );
```

## CI/CD Pipeline

The project includes GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. **Tests both frontend and backend**
2. **Runs security scans**
3. **Deploys to production on main branch push**
4. **Sends notifications**

### Required GitHub Secrets

Add these secrets to your GitHub repository:

```env
# Vercel
VERCEL_TOKEN=your-vercel-token
ORG_ID=your-vercel-org-id
PROJECT_ID=your-vercel-project-id

# Railway  
RAILWAY_TOKEN=your-railway-token
RAILWAY_SERVICE_ID=your-railway-service-id

# URLs for health checks
BACKEND_URL=https://your-backend-url.railway.app
FRONTEND_URL=https://your-frontend-url.vercel.app

# Optional: Notifications
SLACK_WEBHOOK=your-slack-webhook-url
SNYK_TOKEN=your-snyk-token
SONAR_TOKEN=your-sonar-token
```

## Monitoring & Maintenance

### 1. Health Checks

Both frontend and backend include health check endpoints:
- Backend: `GET /health`
- Frontend: Vercel automatically monitors

### 2. Logging

- **Railway**: Built-in logging dashboard
- **Vercel**: Built-in function logs
- **Recommended**: Add Sentry for error tracking

### 3. Performance Monitoring

- **Vercel Analytics**: Automatic performance monitoring
- **Railway Metrics**: Database and API performance
- **Recommended**: Add New Relic or DataDog

### 4. Backups

- **Database**: Supabase automatic backups
- **Code**: Git repository backups
- **Environment**: Document all environment variables

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Verify `ALLOWED_ORIGINS` includes your frontend domain
   - Check Vercel domain configuration

2. **Database Connection Issues**
   - Verify Supabase URL and key
   - Check network connectivity
   - Verify database schema

3. **Authentication Issues**
   - Verify JWT_SECRET_KEY is set
   - Check token expiration settings
   - Verify user permissions

4. **Build Failures**
   - Check Node.js/Python versions
   - Verify all dependencies are installed
   - Check environment variables

### Getting Help

1. **Check logs** in Railway/Vercel dashboards
2. **Review CI/CD pipeline** results
3. **Test locally** with production environment variables
4. **Contact support** via GitHub issues

## Security Checklist

- [ ] JWT secret key is secure and unique
- [ ] Database has Row Level Security enabled
- [ ] HTTPS is enforced on all domains
- [ ] Environment variables are properly secured
- [ ] API rate limiting is configured
- [ ] Security headers are set (see `vercel.json`)
- [ ] Dependencies are regularly updated
- [ ] Vulnerability scanning is enabled

## Performance Optimization

### Frontend
- [ ] Static assets are cached
- [ ] Images are optimized
- [ ] Code splitting is implemented
- [ ] Bundle size is minimized

### Backend
- [ ] Database queries are optimized
- [ ] API responses are cached where appropriate
- [ ] Database indexes are properly set
- [ ] Connection pooling is configured

---

**Need help?** Open an issue on GitHub or check the main README.md for more information.