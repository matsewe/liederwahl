from fastapi import FastAPI, Request
from app.routers import admin, user, songs
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(songs.router)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, session_id : str = ""):
    if session_id == "":
        return templates.TemplateResponse(
            request=request, name="landing.html"
        )
    else:
        return templates.TemplateResponse(
            request=request, name="voting.html"
        )

# 1PMy17eraogNUz436w3aZKxyij39G1didaN02Ka_-45Q
# 71046222