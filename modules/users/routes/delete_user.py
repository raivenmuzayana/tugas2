# File: modules/users/routes/delete_user.py

from fastapi import APIRouter, Depends, HTTPException, status
from modules.users import utils # <-- UBAH IMPORT INI

router = APIRouter()

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(utils.is_admin)], tags=["Users"])
def delete_user(user_id: int):
    db_user = utils.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    utils.fake_users_db.remove(db_user)
    return