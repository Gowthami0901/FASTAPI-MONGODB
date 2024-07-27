# routes/admin.py

from fastapi import APIRouter, Depends
from dependencies import role_required
from auth import TokenData, verify_token

router = APIRouter()

@router.get("/admin-only")
async def admin_only_endpoint(token_data: TokenData = Depends(role_required(["admin"]))):
    return {"message": "Welcome, admin!"}

@router.get("/user-or-admin")
async def user_or_admin_endpoint(token_data: TokenData = Depends(role_required(["user", "admin"]))):
    return {"message": "Welcome, user or admin!"}
