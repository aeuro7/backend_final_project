from fastapi import FastAPI
from app.routers import core_router, pdf_router, quiz_router

app = FastAPI(title="PDF to Quiz API")

app.include_router(pdf_router.router)
app.include_router(quiz_router.router)
app.include_router(core_router.router)
