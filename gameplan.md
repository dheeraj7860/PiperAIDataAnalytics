# Piper Alpha Training Progress Tracking System

## Project Overview
A full-stack application for tracking training progress in the Piper Alpha VR training simulation. Unity game sends performance data to FastAPI backend, users view progress and download reports via Streamlit frontend.

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (Railway-hosted)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens with passlib/bcrypt for password hashing
- **PDF Generation**: ReportLab

### Frontend
- **Framework**: Streamlit
- **Authentication**: JWT token-based with session state

### Deployment
- **Platform**: Railway
- **Database**: Railway PostgreSQL

---

## Database Schema

### Users Table
- `email` (VARCHAR, PRIMARY KEY, UNIQUE) - User's email address
- `hashed_password` (VARCHAR) - bcrypt hashed password
- `role` (VARCHAR) - Either "Trainee" or "Admin"
- `trainee_name` (VARCHAR) - Full name of the trainee (displayed on reports)

### PerformanceData Table
- `id` (INTEGER, PRIMARY KEY, AUTO_INCREMENT) - Unique identifier
- `email` (VARCHAR, FOREIGN KEY to Users) - Reference to user
- `session_timestamp` (TIMESTAMP) - Auto-generated when data is submitted
- `chapter_data` (JSON) - Stores array of chapter performance data

---

## API Endpoints

### Authentication Endpoints (Require Auth)
1. **POST /register**
   - Body: `{email, password, role, trainee_name}`
   - Returns: Success message
   - Validates: Email uniqueness, role values

2. **POST /login**
   - Body: `{email, password}`
   - Returns: `{access_token, token_type}`
   - Authentication: JWT token

### Performance Data Endpoints
3. **POST /performance** (No Auth Required)
   - Body: `{email, chapters: [{chapter, score, status}]}`
   - Validates: User exists, chapter names match allowed list, score 0-10
   - Auto-fills: Missing chapters with score="NA", status="Not Completed"
   - Auto-generates: session_timestamp
   - Returns: Success message with session_id

4. **GET /performance/{email}** (Requires Auth)
   - Returns: All performance sessions for the user
   - Response: `[{session_id, session_timestamp, chapter_data}]`

5. **GET /download-report/{session_id}** (Requires Auth)
   - Generates PDF report matching design
   - Returns: PDF file download

---

## Data Specifications

### Chapters (Exactly 7, case-sensitive)
1. Briefing Room
2. Arrival on Piper Alpha
3. Maintenance Area
4. Precursor to Disaster
5. Explosion Simulation
6. Escape Aftermath
7. Debrief

### Score Range
- Type: Integer
- Range: 0-10
- Missing: "NA" (string)

### Status Values
- "Completed"
- "Pending"
- "Not Completed" (default for missing chapters)

### Example POST Request from Unity Game
```json
{
  "email": "r.example@gmail.com",
  "chapters": [
    {
      "chapter": "Briefing Room",
      "score": 8,
      "status": "Completed"
    },
    {
      "chapter": "Arrival on Piper Alpha",
      "score": 6,
      "status": "Completed"
    },
    {
      "chapter": "Maintenance Area",
      "score": 5,
      "status": "Pending"
    }
  ]
}
```

**Backend Auto-fills Missing Chapters:**
- Explosion Simulation: score="NA", status="Not Completed"
- Precursor to Disaster: score="NA", status="Not Completed"
- Escape Aftermath: score="NA", status="Not Completed"
- Debrief: score="NA", status="Not Completed"

---

## PDF Report Design

### Report Structure (Matching Reference PDF)
1. **Header Section**
   - Title: "COURSE PROGRESS REPORT"
   - Subtitle: "PIPER ALPHA"
   - Logo placeholder (top-left)

2. **Trainee Details Section**
   - Trainee Name: [trainee_name from database]
   - Email: [email]
   - Session Date: [session_timestamp]

3. **Performance Table**
   - 3 Columns: Chapter | Score | Status
   - 7 Rows (one per chapter)
   - Styling: Bordered table, alternating row colors

4. **Remarks Section**
   - Auto-generated based on completion rate
   - Example: "Trainee has completed 3 out of 7 chapters with an average score of 6.3"

---

## Streamlit Frontend Features

### Pages
1. **Login/Register Page**
   - Toggle between login and register
   - Register form: email, password, confirm password, role dropdown, trainee name
   - Login form: email, password
   - JWT token stored in session state

2. **User Dashboard**
   - Welcome message with trainee name
   - List of all performance sessions
   - Each row: `[Session Timestamp] [Download Button]`
   - Download button triggers PDF generation and download

3. **Admin Dashboard (Optional)**
   - View all users
   - View all sessions across users
   - Download any report

---

## Security & Validation

### Password Security
- Hashed using bcrypt via passlib
- Minimum 8 characters (enforced on frontend and backend)

### API Security
- Login/Register: Public endpoints
- Performance submission: Public but validates user exists
- Data retrieval & PDF download: Requires valid JWT token
- JWT expires after 30 days

### Data Validation
- Chapter names must match exactly (case-sensitive)
- Score must be integer 0-10 or "NA"
- Status must be one of: Completed, Pending, Not Completed
- Email must be valid format
- Role must be "Trainee" or "Admin"

---

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key-for-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30
API_BASE_URL=http://localhost:8000
```

---

## Deployment on Railway

### Steps
1. Push code to GitHub repository
2. Create new Railway project
3. Add PostgreSQL database service
4. Add web service from GitHub repo
5. Configure environment variables
6. Deploy FastAPI backend
7. Deploy Streamlit frontend as separate service

### Railway Configuration
- FastAPI: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Streamlit: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

## Future Enhancements (Optional)
- Admin panel to manage users
- Email notifications on report generation
- Data analytics dashboard
- Export data as CSV/Excel
- Multi-language support
- Custom remarks editing
- Performance comparison charts