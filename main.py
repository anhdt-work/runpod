from fastapi import FastAPI
from controller.user import router as user_router
from controller.auth import router as auth_router

app = FastAPI(wagger_ui_parameters={"syntaxHighlight": False})

app.include_router(user_router)
app.include_router(auth_router)
