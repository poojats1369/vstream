python -m venv venv
.\venv\Scripts\activate 
pip install -r requirements.txt

uvicorn app:app --reload 
    # to run the code on 8000 port(default port)

uvicorn app:app --port 8001 --reload # vstream-user-acc
    # change the port no accordingly, check .env file for the port no