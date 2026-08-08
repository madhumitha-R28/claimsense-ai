from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from ai_model import analyze_claim
from schemas import ClaimCreate, UserCreate
from database import claims_collection, users_collection
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

app = FastAPI()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "ClaimSense AI API is running"
    }


# ============================================================
# CREATE CLAIM + AI ANALYSIS
# ============================================================

@app.post("/claims")
def create_claim(
    claim: ClaimCreate,
    current_user: str = Depends(get_current_user)
):
    claim_data = claim.model_dump()

    # Store logged-in username
    claim_data["username"] = current_user

    # Initial claim status
    claim_data["status"] = "Pending"

    # Store creation time
    claim_data["created_at"] = datetime.utcnow()

    # ---------------- AI CLAIM ANALYSIS ----------------

    analysis = analyze_claim(
        claim.claim_amount,
        claim.diagnosis
    )

    claim_data["fraud_risk_score"] = analysis["fraud_risk_score"]
    claim_data["fraud_risk_level"] = analysis["fraud_risk_level"]
    claim_data["decision"] = analysis["decision"]

    # ---------------------------------------------------

    result = claims_collection.insert_one(claim_data)

    return {
        "message": "Claim created successfully",
        "claim_id": str(result.inserted_id),
        "analysis": analysis
    }


# ============================================================
# GET USER CLAIMS
# ============================================================

@app.get("/claims")
def get_claims(
    current_user: str = Depends(get_current_user)
):
    # Return only claims belonging to logged-in user
    claims = list(
        claims_collection.find(
            {"username": current_user}
        )
    )

    for claim in claims:
        claim["_id"] = str(claim["_id"])

    return {
        "claims": claims
    }


# ============================================================
# GET SINGLE CLAIM
# ============================================================

@app.get("/claims/{claim_id}")
def get_claim(
    claim_id: str,
    current_user: str = Depends(get_current_user)
):
    # Validate MongoDB ObjectId
    if not ObjectId.is_valid(claim_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid claim ID"
        )

    # Find claim only if it belongs to logged-in user
    claim = claims_collection.find_one(
        {
            "_id": ObjectId(claim_id),
            "username": current_user
        }
    )

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    claim["_id"] = str(claim["_id"])

    return claim


# ============================================================
# UPDATE CLAIM
# ============================================================

@app.put("/claims/{claim_id}")
def update_claim(
    claim_id: str,
    claim: ClaimCreate,
    current_user: str = Depends(get_current_user)
):
    # Validate MongoDB ObjectId
    if not ObjectId.is_valid(claim_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid claim ID"
        )

    # Re-analyze the updated claim
    analysis = analyze_claim(
        claim.claim_amount,
        claim.diagnosis
    )

    updated_data = claim.model_dump()

    # Keep existing user ownership
    updated_data["username"] = current_user

    # Recalculate status and AI results
    updated_data["status"] = "Pending"
    updated_data["fraud_risk_score"] = analysis["fraud_risk_score"]
    updated_data["fraud_risk_level"] = analysis["fraud_risk_level"]
    updated_data["decision"] = analysis["decision"]

    # Update only if the claim belongs to logged-in user
    result = claims_collection.update_one(
        {
            "_id": ObjectId(claim_id),
            "username": current_user
        },
        {
            "$set": updated_data
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    return {
        "message": "Claim updated successfully",
        "analysis": analysis
    }


# ============================================================
# DELETE CLAIM
# ============================================================

@app.delete("/claims/{claim_id}")
def delete_claim(
    claim_id: str,
    current_user: str = Depends(get_current_user)
):
    # Validate MongoDB ObjectId
    if not ObjectId.is_valid(claim_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid claim ID"
        )

    # Delete only if claim belongs to logged-in user
    result = claims_collection.delete_one(
        {
            "_id": ObjectId(claim_id),
            "username": current_user
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    return {
        "message": "Claim deleted successfully"
    }


# ============================================================
# REGISTER
# ============================================================

@app.post("/register")
def register(user: UserCreate):

    # Check whether username already exists
    existing_user = users_collection.find_one(
        {"username": user.username}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Hash password before storing
    hashed_password = hash_password(user.password)

    users_collection.insert_one({
        "username": user.username,
        "password": hashed_password
    })

    return {
        "message": "User registered successfully"
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    # Find user
    existing_user = users_collection.find_one(
        {"username": form_data.username}
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Verify password
    password_valid = verify_password(
        form_data.password,
        existing_user["password"]
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create JWT access token
    access_token = create_access_token({
        "sub": form_data.username
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }