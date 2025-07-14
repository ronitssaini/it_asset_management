from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from backend.dependencies import get_db
from backend.models.user import User
from backend.auth.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    verify_password,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)
from backend.auth.dependencies import admin_required
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import secrets
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from backend.database.session import SessionLocal

router = APIRouter(tags=["auth"])

# Mailtrap SMTP config (replace with your own if needed)
# conf = ConnectionConfig(
#     MAIL_USERNAME = "your_mailtrap_username",
#     MAIL_PASSWORD = "your_mailtrap_password",
#     MAIL_FROM = "babelokh@gmail.com",
#     MAIL_PORT = 587,
#     MAIL_SERVER = "sandbox.smtp.mailtrap.io",
#     MAIL_FROM_NAME = "IT Asset Dashboard",
#     MAIL_TLS = True,
#     MAIL_SSL = False,
#     USE_CREDENTIALS = True
# )

Base = declarative_base()

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)

# Create the table if it doesn't exist
try:
    PasswordResetToken.__table__.create(bind=SessionLocal().get_bind(), checkfirst=True)
except Exception:
    pass

# Helper to send reset email
def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8000/reset-password?token={token}"
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"""
        <h3>Password Reset Request</h3>
        <p>Click the link below to reset your password. This link will expire in 10 minutes.</p>
        <a href='{reset_link}'>{reset_link}</a>
        <p>If you did not request this, please ignore this email.</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    return fm.send_message(message)

class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  # 'admin' or 'manager'

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    class Config:
        from_attributes = True

@router.post("/register", response_model=UserOut)
def register_user(user: RegisterUserRequest, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        is_active=False  # Needs admin approval
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/pending", response_model=List[UserOut])
def list_pending_users(db: Session = Depends(get_db), role: str = Depends(admin_required)):
    return db.query(User).filter(User.is_active == False).all()

@router.get("/users/pending/count")
def get_pending_users_count(db: Session = Depends(get_db), role: str = Depends(admin_required)):
    count = db.query(User).filter(User.is_active == False).count()
    return {"count": count}

@router.post("/users/approve/{user_id}", response_model=UserOut)
def approve_user(user_id: int, db: Session = Depends(get_db), role: str = Depends(admin_required)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if getattr(user, "is_active"):
        raise HTTPException(status_code=400, detail="User is already active.")
    setattr(user, "is_active", True)
    db.commit()
    db.refresh(user)
    return user

@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not getattr(user, "is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not approved by admin yet.",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users", response_model=List[UserOut])
def list_all_users(db: Session = Depends(get_db), role: str = Depends(admin_required)):
    return db.query(User).all()

@router.delete("/users/reject/{user_id}")
def reject_user(user_id: int, db: Session = Depends(get_db), role: str = Depends(admin_required)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(user)
    db.commit()
    return {"detail": "User registration rejected and deleted."}

# Forgot Password Endpoint (updated)
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        # Generate token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        # Remove old tokens for this user
        db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).delete()
        db.add(PasswordResetToken(user_id=user.id, token=token, expires_at=expires_at))
        db.commit()
        # Send email
        send_reset_email(user.email, token)
    return {"message": "If this email exists, a reset link has been sent."}