python -m venv venv
.\venv\Scripts\activate 
pip install -r requirements.txt

uvicorn app:app --reload 
    # to run the code on 8000 port(default port)

uvicorn app:app --port 8000 --reload # vstream-auth
uvicorn app:app --port 8001 --reload # vstream-user-acc
uvicorn app:app --port 8002 --reload # vstream-user-profile
uvicorn app:app --port 8003 --reload # vstream-static-screen
uvicorn app:app --port 8004 --reload # vstream-file-service
    # change the port no accordingly, check .env file for the port no