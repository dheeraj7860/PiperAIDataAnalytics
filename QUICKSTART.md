# 🚀 Quick Start Guide - Piper Alpha Training System

## Get Up and Running in 5 Minutes!

### Step 1: Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend (in new terminal)
cd frontend
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create `.env` file in project root:

```bash
# Copy template
cp env.example .env

# Generate secret key (run in terminal)
python -c "import secrets; print(secrets.token_hex(32))"
```

Edit `.env`:
```env
DATABASE_URL=sqlite:///./piper_alpha.db
SECRET_KEY=<paste-generated-key-here>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30
API_BASE_URL=http://localhost:8000
```

### Step 3: Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000
✅ API Docs at: http://localhost:8000/docs

### Step 4: Start Frontend (New Terminal)

```bash
cd frontend
streamlit run app.py
```

✅ Frontend running at: http://localhost:8501

### Step 5: Test the System

1. **Open Frontend**: http://localhost:8501
2. **Register**: Create account with Trainee role
3. **Test Unity Integration**:

```bash
# Submit test performance data
curl -X POST http://localhost:8000/performance \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "chapters": [
      {"chapter": "Briefing Room", "score": 8, "status": "Completed"},
      {"chapter": "Arrival on Piper Alpha", "score": 7, "status": "Completed"}
    ]
  }'
```

4. **Login to Dashboard**: See your sessions
5. **Download PDF**: Click download button

---

## 📡 API Endpoints Quick Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/register` | POST | No | Register new user |
| `/login` | POST | No | Get JWT token |
| `/me` | GET | Yes | Get current user |
| `/performance` | POST | No | Submit data (Unity) |
| `/performance/{email}` | GET | Yes | Get user sessions |
| `/download-report/{session_id}` | GET | Yes | Download PDF |
| `/admin/users` | GET | Admin | List all users |
| `/admin/all-sessions` | GET | Admin | All sessions |

---

## 🎮 Unity Integration Example

```csharp
// In your Unity script
string apiUrl = "http://localhost:8000/performance";
string userEmail = "user@example.com";

// Create JSON payload
string json = @"{
    ""email"": """ + userEmail + @""",
    ""chapters"": [
        {""chapter"": ""Briefing Room"", ""score"": 8, ""status"": ""Completed""},
        {""chapter"": ""Arrival on Piper Alpha"", ""score"": 7, ""status"": ""Completed""}
    ]
}";

// Send POST request
UnityWebRequest.Post(apiUrl, json, "application/json");
```

---

## 📋 Valid Chapter Names (Copy-Paste Ready)

```
Briefing Room
Arrival on Piper Alpha
Maintenance Area
Precursor to Disaster
Explosion Simulation
Escape Aftermath
Debrief
```

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is available
# Windows:
netstat -ano | findstr :8000
# Linux/Mac:
lsof -i :8000
```

### Frontend won't connect to backend?
- Check `API_BASE_URL` in frontend
- Make sure backend is running
- Check CORS settings in `backend/app/main.py`

### Database errors?
```bash
# Delete database and restart
rm piper_alpha.db
# Backend will recreate tables on startup
```

### JWT token errors?
- Ensure `SECRET_KEY` is set in `.env`
- Token expires after 30 days (re-login)

---

## 🚢 Deploy to Railway

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push
```

### 2. Create Railway Project
- Add PostgreSQL database
- Deploy backend from `backend/` folder
- Deploy frontend from `frontend/` folder

### 3. Set Environment Variables

**Backend:**
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=<generate-new-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30
```

**Frontend:**
```
API_BASE_URL=<your-backend-url>
```

---

## 📚 Documentation

- **Full README**: `README.md`
- **Project Specs**: `gameplan.md`
- **Implementation Tasks**: `todo.md`
- **API Docs**: http://localhost:8000/docs (when running)

---

## ✅ What's Implemented

- ✅ User registration & authentication (JWT)
- ✅ Role-based access (Trainee/Admin)
- ✅ Performance data submission from Unity
- ✅ Auto-fill missing chapters
- ✅ PDF report generation (matching design)
- ✅ Streamlit dashboard
- ✅ Session management
- ✅ Download reports
- ✅ Admin endpoints
- ✅ Railway deployment ready

---

## 🎯 Next Steps

1. **Customize PDF Design**: Edit `backend/app/pdf_generator.py`
2. **Add Logo**: Replace logo placeholder in PDF generator
3. **Deploy to Production**: Follow Railway deployment guide
4. **Integrate with Unity**: Use provided Unity code examples
5. **Test with Real Users**: Register trainees and collect data

---

## 💡 Tips

- Use **SQLite** for local development (no PostgreSQL needed)
- **PostgreSQL** recommended for production
- JWT tokens last **30 days** - users don't need to login frequently
- **Admin users** can view all user data
- **No auth required** for Unity to submit data (validates user exists)
- Missing chapters automatically filled as **NA / Not Completed**

---

## 📞 Need Help?

Check the full documentation in `README.md` or open an issue on GitHub.

**Happy Training! 🎓**

