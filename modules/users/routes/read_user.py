from fastapi import APIRouter, Depends, HTTPException, Header, status
from typing import List, Optional
from modules.users.schema import schemas
from modules.users import utils

router = APIRouter()

@router.get("/users/", response_model=List[schemas.User], dependencies=[Depends(utils.is_admin)], tags=["Users"])
def read_users():
    return [ {k: v for k, v in user.items() if k != 'hashed_password'} for user in utils.fake_users_db ]

@router.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, x_user_id: Optional[int] = Header(None), x_user_role: Optional[str] = Header(None)):
    db_user = utils.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if x_user_role == schemas.UserRole.admin:
        pass
    elif x_user_role == schemas.UserRole.staff:
        if x_user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only access your own data")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    response_user = db_user.copy()
    del response_user["hashed_password"]
    return response_user