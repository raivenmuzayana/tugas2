from fastapi import FastAPI
from modules.users.routes import create_user, read_user, update_user, delete_user

app = FastAPI(title="User Management API")

app.include_router(create_user.router)
app.include_router(read_user.router)
app.include_router(update_user.router)
app.include_router(delete_user.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the User Management API"}