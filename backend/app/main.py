from fastapi import FastAPI
from .api.routes import router

app = FastAPI(title="Space Debris Dashboard API")
app.include_router(router)
