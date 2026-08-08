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