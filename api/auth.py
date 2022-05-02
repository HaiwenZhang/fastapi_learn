from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import pbkdf2_sha256
from api.db import User, database
from api.toten import create_access_token

router = APIRouter(
    tags = ["Auth"]
)

@router.post("/login")
async def login(request:  OAuth2PasswordRequestForm = Depends()):
    query = User.select().where(User.c.username == request.username)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )

    if not pbkdf2_sha256.verify(request.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Invalid password"
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}