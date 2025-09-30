from fastapi import APIRouter, HTTPException, status
from modules.users.schema import schemas
from modules.users import utils 
from datetime import datetime, timezone

router = APIRouter()

@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: schemas.UserCreate):
    if utils.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
        
    hashed_password = utils.pwd_context.hash(user.password)
    
    new_user = {
        "id": utils.user_id_counter,
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    utils.fake_users_db.append(new_user)
    
    utils.user_id_counter += 1
    
    response_user = new_user.copy()
    del response_user["hashed_password"]
    return response_user