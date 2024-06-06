from app.routers import admin
from app.database import engine, Base, get_db, SessionLocal
import asyncio

def reset():
    #Base.metadata.drop_all(engine)
    #Base.metadata.create_all(engine)
    with SessionLocal() as db:
        asyncio.run(admin.create_upload_file(include_non_singable=True, db=db))