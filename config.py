import os

from dotenv import load_dotenv

load_dotenv()

MAX_PAGE_SIZE = 30

DB_URL = os.getenv("DATABASE_URL")
TEST_DB_URL = 'sqlite:///:memory:'
DB_ECHO = True
