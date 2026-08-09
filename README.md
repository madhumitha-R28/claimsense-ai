# ClaimSense AI

## AI-Powered Insurance Claims Automation Platform

ClaimSense AI is a full-stack insurance claims application that allows authenticated users to submit and manage insurance claims while using an AI-based analysis module to evaluate potential fraud risk.

## Features

- User registration and login
- Secure password hashing
- JWT-based authentication
- Protected REST APIs
- User-specific claim access
- Create, read, update and delete claims
- AI-based claim analysis
- Fraud risk score generation
- Fraud risk level classification
- Automated claim decision
- React-based dashboard
- MongoDB database integration
- FastAPI backend

## Technology Stack

### Frontend
- React
- Vite
- Axios
- HTML
- CSS

### Backend
- Python
- FastAPI
- REST APIs
- JWT Authentication
- Passlib / bcrypt

### Database
- MongoDB
- PyMongo

### AI
- Python-based claim analysis module

## System Architecture

React Frontend
        |
        | REST API
        ↓
FastAPI Backend
        |
        +---- JWT Authentication
        |
        +---- Claim Processing
        |
        +---- AI Claim Analysis
        |
        ↓
MongoDB

## Project Structure

```text
claimsense-ai/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── schemas.py
│   ├── ai_model.py
│   ├── requirements.txt
│   └── .env
│
├── src/
│   ├── App.jsx
│   ├── App.css
│   └── ...
│
├── public/
├── package.json
├── package-lock.json
├── vite.config.js
└── README.md
## How to Run

### Before Starting

Checklist:

- [ ] MongoDB Atlas cluster is running
- [ ] Current IP address is allowed in MongoDB Atlas
- [ ] Database connection configuration is correct
- [ ] Backend dependencies are installed
- [ ] Frontend dependencies are installed

---

### Terminal 1 — Frontend

```powershell
cd C:\Users\madhu\OneDrive\Desktop\claimsense-ai
npm run dev

Frontend will run at:

http://localhost:5173
Terminal 2 — Backend
cd C:\Users\madhu\OneDrive\Desktop\claimsense-ai\backend
python -m uvicorn main:app --reload

Backend will run at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs
If MongoDB Connection Fails

Check MongoDB Atlas:

 Cluster is running
 Current IP address is added
 Database username/password are correct
 MongoDB connection string is correct

Then restart the backend.