# File: modules/users/routes/update_user.py

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
from modules.users.schema import schemas
from modules.users import utils # <-- UBAH IMPORT INI

router = APIRouter()

@router.put("/users/{user_id}", response_model=schemas.User, dependencies=[Depends(utils.is_admin)], tags=["Users"])
def update_user(user_id: int, user_update: schemas.UserUpdate):
    db_user = utils.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        db_user[key] = value
    
    db_user["updated_at"] = datetime.now(timezone.utc)

    response_user = db_user.copy()
    del response_user["hashed_password"]
    return response_user