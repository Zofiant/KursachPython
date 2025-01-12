from datetime import datetime
from app.config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException, Request, Depends, status
from jose import jwt, JWTError

from app.users.repository import UserRepository


def get_token(request: Request):
    token = request.cookies.get("login_access_token")
    if not token: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="none jwt token")
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT token is wrong")
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Expired")
    
    user_id:str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not UserID")
    user =  await UserRepository.find_by_id(int(user_id))
    return user
    