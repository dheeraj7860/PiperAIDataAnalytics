# 🚂 Railway Deployment Guide for Piper Alpha Training System

This guide walks you through deploying the Piper Alpha Training System to Railway.

## 📋 Prerequisites

- [ ] GitHub account
- [ ] Railway account (sign up at [railway.app](https://railway.app))
- [ ] Your code pushed to a GitHub repository

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Ensure all files are committed:**
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

2. **Verify these files exist:**
- ✅ `runtime.txt` (root, backend, frontend)
- ✅ `railway.json` (root)
- ✅ `Procfile` (root, frontend)
- ✅ `requirements.txt` (backend, frontend)
- ✅ `env.example`

---

### Step 2: Create New Railway Project

1. Go to [railway.app](https://railway.app) and log in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `PiperAIDataAnalytics` repository
5. Railway will create an empty project

---

### Step 3: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will provision a PostgreSQL instance
4. Note: The `DATABASE_URL` will be automatically available as `${{Postgres.DATABASE_URL}}`

---

### Step 4: Deploy Backend Service

1. Click **"+ New"** → **"GitHub Repo"** → Select your repo again
2. Configure the service:
   - **Service Name:** `backend`
   - **Root Directory:** `backend`
   - **Build Command:** (auto-detected)
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables:**
   - Click on the backend service
   - Go to **"Variables"** tab
   - Add the following:

   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   SECRET_KEY=<GENERATE_A_SECURE_KEY>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_DAYS=30
   ```

   **Generate SECRET_KEY:**
   ```bash
   # Run this in your terminal:
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Enable Public Networking:**
   - Go to **"Settings"** tab
   - Under **"Networking"**, click **"Generate Domain"**
   - Copy your backend URL (e.g., `https://backend-production-xxxx.up.railway.app`)

5. **Wait for deployment** (2-3 minutes)
   - Check logs to ensure it starts successfully
   - Visit `https://your-backend-url.railway.app/docs` to verify

---

### Step 5: Deploy Frontend Service

1. Click **"+ New"** → **"GitHub Repo"** → Select your repo again
2. Configure the service:
   - **Service Name:** `frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** (auto-detected)
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

3. **Add Environment Variables:**
   ```
   API_BASE_URL=https://your-backend-url.railway.app
   ```
   (Replace with your actual backend URL from Step 4)

4. **Enable Public Networking:**
   - Go to **"Settings"** tab
   - Click **"Generate Domain"**
   - Copy your frontend URL (e.g., `https://frontend-production-xxxx.up.railway.app`)

5. **Wait for deployment** (2-3 minutes)

---

### Step 6: Update CORS Settings (Important!)

Once you have your frontend URL, update the backend to allow it:

1. **Locally, edit `backend/app/config.py`:**
   ```python
   # CORS Origins (for frontend)
   CORS_ORIGINS: list = [
       "http://localhost:8501", 
       "http://127.0.0.1:8501",
       "https://your-frontend-url.railway.app"  # Add this line
   ]
   ```

2. **Or better yet, add it as an environment variable in Railway:**
   - In backend service, add variable:
   ```
   CORS_ORIGINS=http://localhost:8501,https://your-frontend-url.railway.app
   ```
   - Then update `config.py` to read from env var (optional enhancement)

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add production CORS origin"
   git push
   ```
   Railway will auto-redeploy.

---

### Step 7: Test Your Deployment

1. **Visit your frontend URL:**
   - `https://your-frontend-url.railway.app`

2. **Register a test user:**
   - Email: `test@example.com`
   - Password: `TestPass123`
   - Role: `Trainee`
   - Name: `Test User`

3. **Login and test features:**
   - View dashboard
   - Submit performance data via API
   - Download PDF reports

4. **Test API directly:**
   - Visit `https://your-backend-url.railway.app/docs`
   - Try the interactive API documentation

---

## 🔧 Environment Variables Summary

### Backend Service

| Variable | Value | Required | Description |
|----------|-------|----------|-------------|
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | ✅ Yes | PostgreSQL connection string |
| `SECRET_KEY` | `<your-generated-key>` | ✅ Yes | JWT signing key (use `secrets.token_hex(32)`) |
| `ALGORITHM` | `HS256` | ✅ Yes | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_DAYS` | `30` | ✅ Yes | Token expiry duration |
| `CORS_ORIGINS` | `https://frontend-url.railway.app` | ⚠️ Recommended | Allowed CORS origins |

### Frontend Service

| Variable | Value | Required | Description |
|----------|-------|----------|-------------|
| `API_BASE_URL` | `https://backend-url.railway.app` | ✅ Yes | Backend API URL |

---

## 🔍 Troubleshooting

### Backend won't start
- **Check logs:** Click on backend service → "Deployments" → Latest deployment → "View Logs"
- **Common issues:**
  - Missing `DATABASE_URL` - Ensure PostgreSQL service is linked
  - Invalid `SECRET_KEY` - Must be a secure random string
  - Port binding - Railway auto-assigns `$PORT`, don't hardcode it

### Frontend can't connect to backend
- **Verify `API_BASE_URL`:** Should be your backend's Railway URL (with https://)
- **Check CORS:** Backend must allow your frontend domain
- **Test backend directly:** Visit `/docs` endpoint to verify it's running

### Database connection errors
- **Ensure PostgreSQL service is running**
- **Check `DATABASE_URL`:** Should be `${{Postgres.DATABASE_URL}}`
- **Verify database tables:** They're created automatically on first startup

### 502 Bad Gateway
- **Service is still deploying:** Wait 2-3 minutes
- **Build failed:** Check build logs for errors
- **Health check failing:** Verify your app listens on `0.0.0.0:$PORT`

---

## 🔄 Updating Your Deployment

Railway automatically redeploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature X"
git push origin main
```

Railway will:
1. Detect the push
2. Rebuild both services
3. Deploy new versions (zero-downtime)

---

## 💰 Cost Estimate

Railway Pricing (as of 2024):
- **Hobby Plan:** $5/month
  - Includes 500 hours of usage
  - Suitable for development/testing
- **Pro Plan:** Pay-as-you-go
  - $0.000231/GB-hour (memory)
  - $0.000463/vCPU-hour

**Estimated Monthly Cost:**
- PostgreSQL database: ~$2-5
- Backend service: ~$2-5  
- Frontend service: ~$2-5
- **Total: ~$10-15/month** for always-on services

---

## 🔐 Security Checklist

Before going to production:

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Restrict `CORS_ORIGINS` to only your frontend domain (remove `"*"`)
- [ ] Use strong database passwords (Railway handles this)
- [ ] Enable Railway's **"Private Networking"** between services
- [ ] Set up **custom domains** with SSL (optional)
- [ ] Enable **two-factor authentication** on Railway account
- [ ] Review and restrict IAM permissions if using team features

---

## 📊 Monitoring

### Railway Dashboard
- **Metrics:** CPU, Memory, Network usage
- **Logs:** Real-time application logs
- **Deployments:** History of all deployments

### Application Monitoring
- Use FastAPI's `/` health check endpoint
- Monitor PDF generation performance
- Track database query performance
- Set up uptime monitoring (e.g., UptimeRobot)

---

## 🎯 Production Best Practices

1. **Environment Management:**
   - Never commit `.env` files
   - Use Railway's variables for all secrets
   - Keep `env.example` updated

2. **Database Backups:**
   - Railway provides automatic backups for PostgreSQL
   - Download manual backups periodically
   - Test restore procedures

3. **Logging:**
   - Use structured logging
   - Monitor error rates
   - Set up alerts for critical issues

4. **Performance:**
   - Enable caching where appropriate
   - Optimize database queries
   - Monitor response times

5. **Security:**
   - Keep dependencies updated
   - Regular security audits
   - Use HTTPS only in production

---

## 📞 Support

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Streamlit Docs:** https://docs.streamlit.io

---

## ✅ Post-Deployment Checklist

- [ ] Backend is accessible at `https://backend-url.railway.app/docs`
- [ ] Frontend is accessible at `https://frontend-url.railway.app`
- [ ] Database connection is working
- [ ] User registration works
- [ ] User login works
- [ ] Performance data submission works
- [ ] PDF report generation works
- [ ] PDF download works
- [ ] All CORS origins are properly configured
- [ ] Environment variables are set correctly
- [ ] Logs show no errors
- [ ] Custom domain configured (optional)

---

## 🎉 You're Done!

Your Piper Alpha Training System is now live on Railway!

- **Frontend:** `https://your-frontend-url.railway.app`
- **Backend API:** `https://your-backend-url.railway.app`
- **API Docs:** `https://your-backend-url.railway.app/docs`

Share your application URL with users and start tracking training progress! 🚀

