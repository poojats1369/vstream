import uvicorn
from api.db import *
from api.rest import *
from utils import *
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

# Load the .env file
load_dotenv()

Base.metadata.create_all(bind=engine)

host= os.environ.get('HOST')
port = os.environ.get('PORT')
app = FastAPI()

app.include_router(users_router)

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