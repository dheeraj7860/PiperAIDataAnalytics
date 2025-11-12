# 🎓 Piper Alpha Training Progress Tracking System

A full-stack application for tracking training progress in the Piper Alpha VR training simulation. The system consists of a FastAPI backend, PostgreSQL database, and Streamlit frontend, designed to receive performance data from a Unity VR game and provide comprehensive progress reports.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)

---

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Locally](#running-locally)
- [API Documentation](#api-documentation)
- [Unity Integration](#unity-integration)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)

---

## ✨ Features

### User Management
- ✅ User registration with email, password, role (Trainee/Admin), and full name
- ✅ JWT token-based authentication (30-day expiry)
- ✅ Secure password hashing with bcrypt
- ✅ Role-based access control

### Performance Tracking
- ✅ Submit training performance data from Unity game (no auth required)
- ✅ Auto-fill missing chapters with "NA" score and "Not Completed" status
- ✅ Store 7 chapters of Piper Alpha training course
- ✅ Track scores (0-10) and status (Completed/Pending/Not Completed)

### Progress Reports
- ✅ Generate professional PDF reports using ReportLab
- ✅ Match reference design with headers, tables, and remarks
- ✅ Download reports for individual training sessions
- ✅ Calculate completion rates and average scores

### Frontend Dashboard
- ✅ Modern Streamlit interface with login/register
- ✅ View all training sessions with timestamps
- ✅ Download PDF reports directly from browser
- ✅ Responsive design with session statistics

---

## 🛠 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production database (SQLite for development)
- **python-jose** - JWT token management
- **passlib** - Password hashing with bcrypt
- **ReportLab** - PDF generation

### Frontend
- **Streamlit** - Interactive web applications
- **Requests** - API communication
- **Pandas** - Data manipulation

### Deployment
- **Railway** - Hosting platform
- **PostgreSQL on Railway** - Managed database

---

## 📁 Project Structure

```
PiperAIDataAnalytics/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── schemas.py           # Pydantic validation schemas
│   │   ├── database.py          # Database configuration
│   │   ├── auth.py              # Authentication utilities
│   │   ├── crud.py              # Database CRUD operations
│   │   ├── config.py            # Application configuration
│   │   └── pdf_generator.py    # PDF report generation
│   ├── requirements.txt
│   └── Procfile
├── frontend/
│   ├── app.py                   # Streamlit application
│   ├── requirements.txt
│   └── Procfile
├── gameplan.md                  # Project specification
├── todo.md                      # Implementation checklist
├── env.example                  # Environment variables template
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- PostgreSQL 15+ (or use SQLite for development)
- Git

### Clone Repository

```bash
git clone https://github.com/yourusername/PiperAIDataAnalytics.git
cd PiperAIDataAnalytics
```

### Backend Setup

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `env.example`):

```bash
cp env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/piper_alpha
# For SQLite (development):
# DATABASE_URL=sqlite:///./piper_alpha.db

# JWT Secret (generate with: openssl rand -hex 32)
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30

# API URL
API_BASE_URL=http://localhost:8000
```

### Generate Secret Key

```bash
# Linux/Mac
openssl rand -hex 32

# Windows (PowerShell)
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🏃 Running Locally

### 1. Start Backend (FastAPI)

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Start Frontend (Streamlit)

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

Frontend will be available at: http://localhost:8501

---

## 📚 API Documentation

### Authentication Endpoints

#### POST `/register`
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "role": "Trainee",
  "trainee_name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "email": "user@example.com",
  "role": "Trainee",
  "trainee_name": "John Doe",
  "created_at": "2024-01-01T12:00:00Z"
}
```

---

#### POST `/login`
Login and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Performance Data Endpoints

#### POST `/performance`
Submit performance data from Unity game (**No Auth Required**).

**Request Body:**
```json
{
  "email": "user@example.com",
  "chapters": [
    {
      "chapter": "Briefing Room",
      "score": 8,
      "status": "Completed"
    },
    {
      "chapter": "Arrival on Piper Alpha",
      "score": 7,
      "status": "Completed"
    }
  ]
}
```

**Response:** `201 Created`
```json
{
  "message": "Performance data submitted successfully",
  "session_id": 1,
  "session_timestamp": "2024-01-01T14:30:00Z"
}
```

**Note:** Missing chapters are auto-filled with `score="NA"` and `status="Not Completed"`.

---

#### GET `/performance/{email}`
Get all performance sessions for a user (**Auth Required**).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "session_timestamp": "2024-01-01T14:30:00Z",
    "chapter_data": [
      {
        "chapter": "Briefing Room",
        "score": 8,
        "status": "Completed"
      },
      // ... all 7 chapters
    ]
  }
]
```

---

#### GET `/download-report/{session_id}`
Download PDF report for a session (**Auth Required**).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:** `200 OK` - PDF file download

---

## 🎮 Unity Integration

### Sending Performance Data from Unity

```csharp
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;

public class PerformanceTracker : MonoBehaviour
{
    private string apiUrl = "http://your-api-url.com/performance";
    
    [System.Serializable]
    public class ChapterData
    {
        public string chapter;
        public int score;
        public string status;
    }
    
    [System.Serializable]
    public class PerformanceSubmit
    {
        public string email;
        public ChapterData[] chapters;
    }
    
    public IEnumerator SubmitPerformance(string userEmail)
    {
        PerformanceSubmit data = new PerformanceSubmit
        {
            email = userEmail,
            chapters = new ChapterData[]
            {
                new ChapterData { 
                    chapter = "Briefing Room", 
                    score = 8, 
                    status = "Completed" 
                },
                new ChapterData { 
                    chapter = "Arrival on Piper Alpha", 
                    score = 7, 
                    status = "Completed" 
                }
                // Add more chapters as needed
            }
        };
        
        string json = JsonUtility.ToJson(data);
        
        using (UnityWebRequest request = UnityWebRequest.Post(apiUrl, json, "application/json"))
        {
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("Performance data submitted successfully!");
            }
            else
            {
                Debug.LogError($"Error: {request.error}");
            }
        }
    }
}
```

### Valid Chapter Names (Case-Sensitive)
1. Briefing Room
2. Arrival on Piper Alpha
3. Maintenance Area
4. Precursor to Disaster
5. Explosion Simulation
6. Escape Aftermath
7. Debrief

---

## 🚢 Deployment

### Deploy to Railway

#### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/PiperAIDataAnalytics.git
git push -u origin main
```

#### 2. Deploy Backend on Railway

1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add **PostgreSQL** service to your project
5. Configure Backend service:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   SECRET_KEY=<generate-secure-key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_DAYS=30
   ```

#### 3. Deploy Frontend on Railway

1. Add new service from same GitHub repo
2. Configure Frontend service:
   - **Root Directory**: `frontend`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
3. Add environment variables:
   ```
   API_BASE_URL=<your-backend-railway-url>
   ```

---

## 🧪 Testing

### Manual Testing

#### 1. Test User Registration
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "role": "Trainee",
    "trainee_name": "Test User"
  }'
```

#### 2. Test Login
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### 3. Test Performance Submission
```bash
curl -X POST http://localhost:8000/performance \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "chapters": [
      {"chapter": "Briefing Room", "score": 8, "status": "Completed"}
    ]
  }'
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

- Your Name - Initial work

---

## 🙏 Acknowledgments

- Piper Alpha VR Training Team
- ReportLab for PDF generation
- FastAPI and Streamlit communities

---

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@piperalphatraining.com

---

## 🔄 Version History

- **v1.0.0** - Initial release
  - User registration and authentication
  - Performance data tracking
  - PDF report generation
  - Streamlit dashboard
  - Railway deployment support

