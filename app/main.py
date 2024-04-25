from fastapi import FastAPI
from app.routers import admin, user

app = FastAPI()

app.include_router(admin.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


# 1PMy17eraogNUz436w3aZKxyij39G1didaN02Ka_-45Q
# 71046222
