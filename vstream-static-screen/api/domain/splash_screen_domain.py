from api.db import *
from utils import *
from api.helper import *
from utils import *

def retrieve_splash_screen_data():
    # Specify the path to the image or GIF file
    file_path = SPLASH_SCREEN_PATH 
    # file_path = "D:/OTT/user/media/splash_screen.gif"  
    
    if not os.path.isfile(file_path):
        return {"success": False}

    # Read the file in binary mode
    with open(file_path, "rb") as file:
        data = file.read()

    # Return the file path and data in the response
    return {
        "success": True,
        "path": file_path,
        "content_type": "image/gif" if file_path.endswith(".gif") else "image/jpeg",
        "data": data
    }