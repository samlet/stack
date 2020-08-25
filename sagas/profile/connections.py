import os
from dotenv import load_dotenv
load_dotenv()

def config():
    return dict(user = os.getenv('postgres_user'),
              password = os.getenv('postgres_password'),
              host = os.getenv('postgres_host'),
              port = os.getenv('postgres_port'),
              database = os.getenv('postgres_database'))

