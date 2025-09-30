from fastapi import HTTPException, Header, status
from passlib.context import CryptContext
from modules.users.schema import schemas

# In-memory "database"
fake_users_db = []
user_id_counter = 1

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Helper Functions ---
def get_user_by_id(user_id: int):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    return None

def get_user_by_username(username: str):
    for user in fake_users_db:
        if user["username"] == username:
            return user
    return None

# --- Dependencies ---
def is_admin(x_user_role: str = Header(...)):
    if x_user_role != schemas.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )