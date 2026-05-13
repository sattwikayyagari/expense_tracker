from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.transaction import router as transacion_router

app=FastAPI()

@app.get("/")
def home():
    return {'status': 'ok?'}

app.include_router(user_router)
app.include_router(transacion_router)