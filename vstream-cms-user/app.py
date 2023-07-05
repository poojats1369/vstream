import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.db import *
from utils import *
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from api.rest import *
from dotenv import load_dotenv

# Load the .env file.
load_dotenv()

Base.metadata.create_all(bind=engine)

host= os.environ.get('HOST')
port = os.environ.get('PORT')

app = FastAPI()

app.include_router(users_router)
app.include_router(roles_router)
app.include_router(permissions_router)
app.include_router(user_activity_router)

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

if __name__ =='__main__':
    uvicorn.run(app, host=host, port=port)