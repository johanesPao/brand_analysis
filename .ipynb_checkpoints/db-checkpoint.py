import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd

class Database:
    def __init__(self):
        load_dotenv()
        self.credentials = {
            "USER": os.environ.get("DB_USER"),
            "PASS": os.environ.get("DB_PASS"),
            "SERVER_SOS": os.environ.get("DB_SERVER_SOS"),
            "SERVER_OMNI": os.environ.get("DB_SERVER_OMNI"),
            "DB_SOS": os.environ.get("DB_NAME_SOS"),
            "DB_ORBIT": os.environ.get("DB_NAME_ORBIT"),
            "DB_OMNI": os.environ.get("DB_NAME_OMNI")
        }

    def print_credentials(self):
        for key, value in self.credentials.items():
            print(f"{key}:{value}")

    def connect(
        self,
        server: str, 
        database: str,
        user: str,
        password: str
    ) -> pyodbc.connect:
        return pyodbc.connect(f"""
            DRIVER={{ODBC Driver 18 for SQL Server}};
            SERVER={server};
            DATABASE={database};
            UID={user};
            PWD={password};
            Authentication=SqlPassword;
        """)

    def sos_conn(self) -> pyodbc.connect:
        return self.connect(
            self.credentials['SERVER_SOS'], 
            self.credentials['DB_SOS'],
            self.credentials['USER'],
            self.credentials['PASS']
        )
        # cursor.execute('SELECT * FROM MS_SHOWROOM')
        # data = cursor.fetchall()
        # df = pd.DataFrame(data)
        # print(df.head(5))
        