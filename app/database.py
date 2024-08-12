from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os



# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv("user")
# print(DB_SERVER)
DB_NAME = os.getenv("dbname")
# print(DB_NAME)
DB_PW = os.getenv("password")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
# print(DB_USERNAME)s

# DB_HOST = os.getenv("host")
# DB_PORT = os.getenv("port")
# serverr = os.getenv('server')
# databasee = os.getenv('database')
# driverr = os.getenv('driver')


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# print(f"Server: {serverr}")
# print(f"Database: {databasee}")
# print(f"Driver: {driverr}")

# print("ODBCINI:", os.environ.get('ODBCINI'))
# print("ODBCSYSINI:", os.environ.get('ODBCSYSINI'))
# print("PATH:", os.environ.get('PATH'))

# dbname = 'postgres'
# user = 'postgres'
# password = '1234'
# host = 'localhost'
# port = 5432

# server = 'DESKTOP-SSDDEM6\\SQL2022TRAINING'
# database = 'learn2'
# driver = 'ODBC Driver 17 for SQL Server'

# Construct the connection URL for Windows Authentication
# DATABASE_URL = f"mssql+pyodbc://@{serverr}/{databasee}?driver={driverr.replace(' ', '+')}&trusted_connection=yes"

# server = 'DESKTOP-SSDDEM6\\SQL2022TRAINING'
# database = 'learn2'

# DATABASE_URL = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"


# DATABASE_URL = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};Trusted_Connection=yes; ENCRYPT=no;"
# DATABASE_URL = f"mssql+pyodbc://{username}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver={driver.replace(' ', '+')}"


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)



SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base() # defines SQLAlchemy models using Python classes.

