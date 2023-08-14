import os
from dotenv import load_dotenv

def load_env(path: str = None):
    if path == None:
        dotenv_path = os.path.join(os.getenv("HOME"), ".env")
    else:
        dotenv_path = path
    load_dotenv(dotenv_path = dotenv_path)