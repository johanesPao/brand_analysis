from dotenv import dotenv_values
import pyodbc

class Database:
    def __init__(self):
        self.credentials = dotenv_values('.credentials.env')
        self.servers = dotenv_values('.servers.env')
        self.databases = dotenv_values('.databases.env')

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
            self.servers['SOS'], 
            self.databases['SOS'],
            self.credentials['USERNAME'],
            self.credentials['PASSWORD']
        )
        