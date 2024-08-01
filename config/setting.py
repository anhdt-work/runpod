import pytz
import os

TIME_ZONE = pytz.timezone("Etc/UTC")
MODEL_ENDPOINT = "http://localhost:9000/endpoint"
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
