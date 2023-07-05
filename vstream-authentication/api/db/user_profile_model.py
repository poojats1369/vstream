import bcrypt
from utils import *
from api.db.schemas import *
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, ARRAY


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(String, index=True, unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    profile_name = Column(String)
    profile_image = Column(Text)
    date_of_birth = Column(String)
    content_language = Column(ARRAY(String))
    app_language = Column(String)
    genre = Column(ARRAY(String))
    _pin = Column("pin", String)
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    is_child = Column(Boolean)
    status = Column(Boolean)

    user = relationship("User", back_populates="profiles")
    watchlist_items = relationship("WatchlistItem", back_populates="user_profile")

     # Custom property to handle pin encryption and decryption
    @property
    def pin(self):
        raise AttributeError("Pin cannot be accessed directly.")

    @pin.setter
    def pin(self, value):
        # Encrypt the pin before storing in the database
        salt = bcrypt.gensalt()
        encoded_pin = bcrypt.hashpw(value.encode(), salt)
        self._pin = encoded_pin.decode()

    def check_pin(self, pin):
        # Check if the provided pin matches the stored encoded pin
        return bcrypt.checkpw(pin.encode(), self._pin.encode())
    

