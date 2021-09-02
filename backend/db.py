import databases
import sqlalchemy

DATABASE = 'postgresql'
USER = 'fast'
PASSWORD = 'password'
HOST = 'database'
PORT = '5432'
DB_NAME = 'fast'

DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

database = databases.Database(DATABASE_URL, min_size=5, max_size=20)

ECHO_LOG = True

engine = sqlalchemy.create_engine(DATABASE_URL, echo=ECHO_LOG)

metadata = sqlalchemy.MetaData()
