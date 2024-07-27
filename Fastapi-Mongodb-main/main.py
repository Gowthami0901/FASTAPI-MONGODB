from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from routes.user import user
from routes.login_router import login_router
from routes.password_reset import password_reset_router
from exceptions.exceptions import InvalidUserException

load_dotenv()

# Retrieve the SECRET_KEY from the environment
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for JWT generation")


app = FastAPI(title="User Management")

# Configure CORS
origins = [
    "*",
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler
@app.exception_handler(InvalidUserException)
async def invalid_user_handler(request: Request, exc: InvalidUserException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Include routers
app.include_router(user)

app.include_router(login_router)
app.include_router(password_reset_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
