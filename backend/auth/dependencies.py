from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from .security import oauth2_scheme, SECRET_KEY, ALGORITHM

# ✅ Extracts role from the token
def get_current_user_role(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role is None:
            raise credentials_exception
        return role
    except JWTError:
        raise credentials_exception

# 🔐 Only for Admin
def admin_required(role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return role

# 🔐 For Admin or Manager
def manager_or_admin_required(role: str = Depends(get_current_user_role)):
    if role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager or admin privileges required"
        )
    return role
