from fastapi import FastAPI
from app.routers import pdf_router, remember , testgpt

app = FastAPI(title="PDF to Quiz API")

app.include_router(pdf_router.router)
app.include_router(remember.router)
app.include_router(testgpt.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}