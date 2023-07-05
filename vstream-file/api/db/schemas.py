from pydantic import BaseModel
from typing import Optional
import enum
# from constants import *

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

class FileSystemSchema(BaseModel):
    object_id: str
    object_type: str
    file_name: str
    path: str
    file_size: int
    duration: Optional[float]
    thumbnail_path: Optional[str]
    description: Optional[str]
    is_public: bool