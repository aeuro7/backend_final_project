from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import remember , understand

app = FastAPI(title="PDF to Quiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(remember.router)
app.include_router(understand.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}