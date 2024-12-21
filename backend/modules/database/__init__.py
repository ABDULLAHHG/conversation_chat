from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load environment variables
mysql_user = os.getenv("mysql_user")
mysql_password = os.getenv("mysql_password")
mysql_host = os.getenv("mysql_host")
mysql_port = os.getenv("mysql_port")
mysql_database = os.getenv("mysql_database")

# Create MySQL engine and session
mysql_engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}')
Session = sessionmaker(bind=mysql_engine)
Base = declarative_base()