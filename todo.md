# Implementation TODO List - Piper Alpha Training System

## Phase 1: Project Setup & Backend Foundation

### ✅ Todo 1: Project Structure Setup
**Status:** Pending  
**Priority:** High  
**Description:** Create the initial project structure and install all required dependencies.

**Tasks:**
- [ ] Create project root directory structure:
  ```
  PiperAIDataAnalytics/
  ├── backend/
  │   ├── app/
  │   │   ├── __init__.py
  │   │   ├── main.py
  │   │   ├── database.py
  │   │   ├── models.py
  │   │   ├── schemas.py
  │   │   ├── auth.py
  │   │   ├── crud.py
  │   │   ├── pdf_generator.py
  │   │   └── config.py
  │   └── requirements.txt
  ├── frontend/
  │   ├── app.py
  │   ├── pages/
  │   │   ├── login.py
  │   │   └── dashboard.py
  │   └── requirements.txt
  ├── .env.example
  ├── .gitignore
  └── README.md
  ```
- [ ] Create `backend/requirements.txt` with:
  ```
  fastapi==0.104.1
  uvicorn[standard]==0.24.0
  sqlalchemy==2.0.23
  psycopg2-binary==2.9.9
  python-jose[cryptography]==3.3.0
  passlib[bcrypt]==1.7.4
  python-multipart==0.0.6
  reportlab==4.0.7
  python-dotenv==1.0.0
  pydantic==2.5.0
  pydantic-settings==2.1.0
  ```
- [ ] Create `frontend/requirements.txt` with:
  ```
  streamlit==1.29.0
  requests==2.31.0
  pandas==2.1.3
  python-dotenv==1.0.0
  ```
- [ ] Create `.gitignore` file
- [ ] Initialize git repository

---

### ✅ Todo 2: Database Models & Configuration
**Status:** Pending  
**Priority:** High  
**Description:** Setup SQLAlchemy models and database connection configuration.

**Tasks:**
- [ ] Create `backend/app/config.py`:
  - Load environment variables
  - Define SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
  - Define DATABASE_URL
- [ ] Create `backend/app/database.py`:
  - Setup SQLAlchemy engine
  - Create SessionLocal for database sessions
  - Create Base declarative class
  - Implement `get_db()` dependency
- [ ] Create `backend/app/models.py`:
  - **User model:**
    - email (String, primary_key, unique, index)
    - hashed_password (String)
    - role (String) - "Trainee" or "Admin"
    - trainee_name (String)
    - created_at (DateTime, default=now)
  - **PerformanceData model:**
    - id (Integer, primary_key, autoincrement)
    - email (String, ForeignKey to User)
    - session_timestamp (DateTime, default=now)
    - chapter_data (JSON)
    - relationship to User model
- [ ] Create database initialization script
- [ ] Test database connection

---

### ✅ Todo 3: Pydantic Schemas
**Status:** Pending  
**Priority:** High  
**Description:** Define request/response schemas for API validation.

**Tasks:**
- [ ] Create `backend/app/schemas.py` with:
  - **UserCreate:** email, password, role, trainee_name
  - **UserLogin:** email, password
  - **Token:** access_token, token_type
  - **ChapterData:** chapter, score (int 0-10 or "NA"), status (Completed/Pending/Not Completed)
  - **PerformanceSubmit:** email, chapters (list of ChapterData)
  - **PerformanceResponse:** session_id, session_timestamp, chapter_data
  - **UserResponse:** email, role, trainee_name
- [ ] Add field validators:
  - Email format validation
  - Role enum validation
  - Chapter name validation (must be one of 7 allowed)
  - Score range validation (0-10)
  - Status enum validation

---

### ✅ Todo 4: Authentication System
**Status:** Pending  
**Priority:** High  
**Description:** Implement JWT authentication with password hashing.

**Tasks:**
- [ ] Create `backend/app/auth.py`:
  - **Password hashing functions:**
    - `get_password_hash(password)` using passlib bcrypt
    - `verify_password(plain_password, hashed_password)`
  - **JWT token functions:**
    - `create_access_token(data: dict, expires_delta: Optional[timedelta])` using python-jose
    - `decode_access_token(token: str)` returns email
  - **Dependency functions:**
    - `get_current_user(token: str, db: Session)` - validates token and returns User
    - `get_current_active_user()` - ensures user exists
- [ ] Define constants:
  - VALID_CHAPTERS list (7 chapter names)
  - VALID_STATUSES list (Completed, Pending, Not Completed)
  - VALID_ROLES list (Trainee, Admin)
- [ ] Test password hashing and token generation

---

## Phase 2: Backend API Development

### ✅ Todo 5: User Registration Endpoint
**Status:** Pending  
**Priority:** High  
**Description:** Create POST /register endpoint for new user registration.

**Tasks:**
- [ ] Create `backend/app/crud.py` with database operations:
  - `get_user_by_email(db: Session, email: str)`
  - `create_user(db: Session, user: UserCreate)`
- [ ] In `backend/app/main.py` create endpoint:
  - Route: `POST /register`
  - Request body: UserCreate schema
  - Validate email uniqueness
  - Validate password length (min 8 chars)
  - Validate role is "Trainee" or "Admin"
  - Hash password using bcrypt
  - Save user to database
  - Return success message
- [ ] Add error handling:
  - 400: Email already registered
  - 400: Invalid role
  - 422: Validation errors
- [ ] Test with different inputs

---

### ✅ Todo 6: User Login Endpoint
**Status:** Pending  
**Priority:** High  
**Description:** Create POST /login endpoint returning JWT token.

**Tasks:**
- [ ] In `backend/app/main.py` create endpoint:
  - Route: `POST /login`
  - Request body: UserLogin schema (email, password)
  - Validate user exists
  - Verify password using bcrypt
  - Generate JWT token with 30-day expiry
  - Return Token schema (access_token, token_type="bearer")
- [ ] Add error handling:
  - 401: Incorrect email or password
  - 404: User not found
- [ ] Test login flow with valid/invalid credentials

---

### ✅ Todo 7: Performance Data Submission Endpoint
**Status:** Pending  
**Priority:** High  
**Description:** Create POST /performance endpoint (no auth required, for Unity game).

**Tasks:**
- [ ] Add to `backend/app/crud.py`:
  - `create_performance_data(db: Session, email: str, chapter_data: list)`
- [ ] In `backend/app/main.py` create endpoint:
  - Route: `POST /performance`
  - Request body: PerformanceSubmit schema
  - **Validation logic:**
    - Check if user with email exists (return 404 if not)
    - Validate all chapter names are in VALID_CHAPTERS
    - Validate scores are 0-10 integers
    - Validate statuses are in VALID_STATUSES
  - **Auto-fill logic:**
    - Get list of submitted chapters
    - For each chapter in VALID_CHAPTERS not submitted:
      - Add entry with score="NA", status="Not Completed"
  - Auto-generate session_timestamp
  - Save to database as JSON
  - Return success with session_id
- [ ] Add error handling:
  - 404: User not found
  - 400: Invalid chapter name
  - 400: Invalid score range
  - 400: Invalid status value
- [ ] Test with partial chapter data

---

### ✅ Todo 8: Get User Performance Data Endpoint
**Status:** Pending  
**Priority:** Medium  
**Description:** Create GET /performance/{email} endpoint (requires auth).

**Tasks:**
- [ ] Add to `backend/app/crud.py`:
  - `get_user_performance_data(db: Session, email: str)`
- [ ] In `backend/app/main.py` create endpoint:
  - Route: `GET /performance/{email}`
  - Requires authentication (use `get_current_user` dependency)
  - Verify logged-in user matches requested email (or is Admin)
  - Fetch all performance records for user
  - Return list of PerformanceResponse
- [ ] Add error handling:
  - 401: Not authenticated
  - 403: Not authorized to view other user's data
  - 404: No data found
- [ ] Test with authenticated requests

---

### ✅ Todo 9: PDF Generation Service
**Status:** Pending  
**Priority:** High  
**Description:** Create PDF generator matching the reference report design.

**Tasks:**
- [ ] Create `backend/app/pdf_generator.py`:
  - **Function:** `generate_course_report(user_data: dict, session_data: dict) -> BytesIO`
  - **Report sections:**
    1. **Header:**
       - Title: "COURSE PROGRESS REPORT" (large, bold, centered)
       - Subtitle: "PIPER ALPHA" (medium, centered)
       - Placeholder logo space (top-left, 80x80)
    2. **Trainee Details Section:**
       - "TRAINEE DETAILS" heading
       - Name: {trainee_name}
       - Email: {email}
       - Session Date: {session_timestamp formatted}
    3. **Performance Table:**
       - Headers: Chapter | Score | Status
       - 7 rows (all chapters in order)
       - Styling: borders, alternating row colors
       - Font: Professional sans-serif
    4. **Remarks Section:**
       - "REMARKS" heading
       - Auto-generate text:
         - Calculate completion rate
         - Calculate average score (exclude "NA")
         - Example: "TRAINEE HAS COMPLETED 5 OUT OF 7 CHAPTERS WITH AN AVERAGE SCORE OF 7.2"
  - **Styling:**
    - Page size: A4
    - Colors: Professional blue/gray palette
    - Fonts: Helvetica Bold for headers, Helvetica for content
- [ ] Create helper function to calculate stats
- [ ] Test PDF generation with sample data
- [ ] Verify PDF matches reference design

---

### ✅ Todo 10: PDF Download Endpoint
**Status:** Pending  
**Priority:** High  
**Description:** Create GET /download-report/{session_id} endpoint (requires auth).

**Tasks:**
- [ ] Add to `backend/app/crud.py`:
  - `get_performance_by_session_id(db: Session, session_id: int)`
- [ ] In `backend/app/main.py` create endpoint:
  - Route: `GET /download-report/{session_id}`
  - Requires authentication
  - Fetch session data by session_id
  - Verify user owns the session (or is Admin)
  - Fetch user details (trainee_name, email)
  - Generate PDF using pdf_generator
  - Return FileResponse with PDF
  - Filename: `PiperAlpha_Report_{trainee_name}_{timestamp}.pdf`
- [ ] Add error handling:
  - 401: Not authenticated
  - 403: Not authorized
  - 404: Session not found
- [ ] Test PDF download flow

---

## Phase 3: Frontend Development (Streamlit)

### ✅ Todo 11: Streamlit Authentication Pages
**Status:** Pending  
**Priority:** High  
**Description:** Create login and registration interface with session management.

**Tasks:**
- [ ] Create `frontend/app.py` main file:
  - Setup page config
  - Initialize session state for auth
  - Route between login/dashboard based on auth status
- [ ] Create `frontend/pages/login.py`:
  - **Login Form:**
    - Email input
    - Password input (type="password")
    - Login button
    - Toggle to registration form
  - **Register Form:**
    - Email input
    - Trainee name input
    - Role dropdown (Trainee/Admin)
    - Password input (type="password")
    - Confirm password input
    - Register button
    - Toggle to login form
  - **API Integration:**
    - POST to `/register` endpoint
    - POST to `/login` endpoint
    - Store JWT token in `st.session_state["token"]`
    - Store user info in `st.session_state["user"]`
  - **Validation:**
    - Password match check
    - Minimum 8 characters
    - Valid email format
  - **Error handling:**
    - Display API error messages with st.error()
- [ ] Add loading states with st.spinner()
- [ ] Test login/register flows

---

### ✅ Todo 12: Streamlit User Dashboard
**Status:** Pending  
**Priority:** High  
**Description:** Create main dashboard displaying user's performance sessions.

**Tasks:**
- [ ] Create `frontend/pages/dashboard.py`:
  - **Header:**
    - Display welcome message with trainee name
    - Logout button (clears session state)
  - **Session List:**
    - Fetch data from `GET /performance/{email}` with auth header
    - Display sessions in table/list format:
      - Columns: Session Date | Chapters Completed | Average Score | Download
    - Sort by session_timestamp descending (newest first)
  - **Empty State:**
    - Show message if no sessions exist
    - Instruction text about how data is submitted from Unity
  - **Error Handling:**
    - Handle network errors
    - Handle auth errors (redirect to login)
- [ ] Style dashboard with custom CSS
- [ ] Add refresh button
- [ ] Test with multiple sessions

---

### ✅ Todo 13: Streamlit PDF Download Functionality
**Status:** Pending  
**Priority:** High  
**Description:** Implement download button for each session.

**Tasks:**
- [ ] In dashboard, add download button for each session:
  - Button with download icon (📥)
  - On click: Call `GET /download-report/{session_id}` with auth
  - Use `st.download_button()` for file download
  - File content: PDF bytes from API
  - Filename: `PiperAlpha_Report_{session_timestamp}.pdf`
- [ ] Add loading spinner during download
- [ ] Handle download errors:
  - Network errors
  - Auth errors
  - Invalid session errors
- [ ] Add success message after download
- [ ] Test download with different browsers

---

### ✅ Todo 14: Admin Features (Optional)
**Status:** Pending  
**Priority:** Low  
**Description:** Create admin dashboard to view all users and sessions.

**Tasks:**
- [ ] Create `frontend/pages/admin.py`:
  - Check if user role is "Admin"
  - **User Management Tab:**
    - List all registered users
    - Show: Email, Name, Role, Registration Date
    - Search/filter functionality
  - **All Sessions Tab:**
    - List all performance sessions across users
    - Show: User Email, Session Date, Completion Rate
    - Filter by user, date range
    - Download button for any report
  - **Statistics Tab:**
    - Total users count
    - Total sessions count
    - Average completion rate
    - Charts (optional)
- [ ] Add backend endpoint `GET /admin/users` (admin only)
- [ ] Add backend endpoint `GET /admin/all-sessions` (admin only)
- [ ] Test admin access control

---

## Phase 4: Configuration & Deployment

### ✅ Todo 15: Environment Configuration
**Status:** Pending  
**Priority:** High  
**Description:** Setup environment variables and configuration files.

**Tasks:**
- [ ] Create `.env.example`:
  ```env
  # Database
  DATABASE_URL=postgresql://user:password@localhost:5432/piper_alpha
  
  # JWT Authentication
  SECRET_KEY=your-secret-key-change-this-in-production
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_DAYS=30
  
  # API Configuration
  API_BASE_URL=http://localhost:8000
  
  # Frontend
  STREAMLIT_SERVER_PORT=8501
  ```
- [ ] Create `.gitignore`:
  - `.env`
  - `__pycache__/`
  - `*.pyc`
  - `*.pyo`
  - `venv/`
  - `.pytest_cache/`
  - `*.db`
- [ ] Document how to generate SECRET_KEY
- [ ] Create local `.env` file (not committed)
- [ ] Test environment variable loading

---

### ✅ Todo 16: API Documentation
**Status:** Pending  
**Priority:** Medium  
**Description:** Add comprehensive API documentation with examples.

**Tasks:**
- [ ] In `backend/app/main.py`:
  - Add FastAPI metadata (title, description, version)
  - Add tags for endpoint grouping
  - Add detailed docstrings to all endpoints
  - Add request/response examples
- [ ] Document error responses
- [ ] Add CORS middleware for frontend access
- [ ] Test Swagger UI at `/docs`
- [ ] Test ReDoc at `/redoc`
- [ ] Create API usage examples in README

---

### ✅ Todo 17: Railway Deployment Setup
**Status:** Pending  
**Priority:** High  
**Description:** Configure project for Railway deployment.

**Tasks:**
- [ ] **Backend Deployment:**
  - Create `Procfile` or configure start command:
    - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Create `railway.json` (optional)
  - Add PostgreSQL service on Railway
  - Configure environment variables on Railway
  - Setup automatic deployments from GitHub
- [ ] **Frontend Deployment:**
  - Configure Streamlit start command:
    - `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
  - Add environment variables (API_BASE_URL)
  - Link to backend service
- [ ] **Database Migrations:**
  - Add Alembic for database migrations (optional)
  - Create initial migration
  - Test migration on Railway
- [ ] Test deployment:
  - Backend health check endpoint
  - Frontend loads correctly
  - Database connection works
  - Authentication flow works
  - PDF generation works

---

### ✅ Todo 18: Testing & Quality Assurance
**Status:** Pending  
**Priority:** High  
**Description:** Comprehensive testing of all features.

**Tasks:**
- [ ] **Backend Testing:**
  - Test all API endpoints with Postman/curl
  - Test user registration (unique email constraint)
  - Test login (valid/invalid credentials)
  - Test performance submission with partial data
  - Test auto-fill of missing chapters
  - Test PDF generation for various data
  - Test authentication on protected endpoints
  - Test admin vs trainee access
- [ ] **Frontend Testing:**
  - Test registration form validation
  - Test login flow
  - Test dashboard data loading
  - Test PDF download
  - Test logout functionality
  - Test error handling (network errors, auth errors)
  - Test on different browsers
- [ ] **Integration Testing:**
  - Test complete flow: Register → Login → Submit data → View dashboard → Download PDF
  - Test Unity game integration (simulate POST request)
  - Test concurrent users
- [ ] **Edge Cases:**
  - Empty database
  - Missing chapters in submission
  - Invalid token
  - Expired token
  - Score="NA" handling in PDF
- [ ] Document test cases and results

---

### ✅ Todo 19: Documentation & README
**Status:** Pending  
**Priority:** Medium  
**Description:** Create comprehensive documentation for the project.

**Tasks:**
- [ ] Create `README.md` with:
  - Project overview
  - Features list
  - Technology stack
  - Prerequisites
  - **Local Development Setup:**
    - Clone repository
    - Install dependencies
    - Setup PostgreSQL
    - Configure environment variables
    - Run database migrations
    - Start backend server
    - Start frontend server
  - **API Documentation:**
    - List all endpoints with examples
    - Authentication flow
    - Unity integration guide
  - **Deployment Guide:**
    - Railway setup steps
    - Environment variables configuration
    - Database setup
  - **Project Structure**
  - **Contributing guidelines**
  - **License**
- [ ] Add inline code comments
- [ ] Create API request examples (curl/Python/JavaScript)
- [ ] Document common issues and troubleshooting
- [ ] Add screenshots of UI

---

## Summary

**Total Tasks:** 19 main todos  
**Estimated Time:** 15-20 hours  
**Priority Breakdown:**
- High Priority: 15 tasks
- Medium Priority: 3 tasks
- Low Priority: 1 task

**Dependencies:**
- Todos 1-4 must be completed first (foundation)
- Todos 5-10 depend on foundation
- Todos 11-14 depend on backend being functional
- Todos 15-19 can be done in parallel with testing

**Next Steps:**
1. Start with Todo 1 (Project Setup)
2. Complete Phase 1 (Backend Foundation)
3. Test Phase 1 thoroughly
4. Move to Phase 2 (API Development)
5. Complete Phase 3 (Frontend)
6. Deploy and test on Railway (Phase 4)

