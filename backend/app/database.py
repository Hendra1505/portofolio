import os
from pathlib import Path
import psycopg2 import pool
from dotenv import load_dotenv

# membuat variabel dari file .env
load_dotenv()

# membuat connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=50,
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME")
)

def get_db_connection():
    """Mengambil koneksi dari pool."""
    return db_pool.getconn()

def release_db_connection(conn):
    """Mengembalikan koneksi ke pool"""
    db_pool.putconn(conn)

class Database(ABC):
    """
    Database context manager
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


# The Database class is defined as a subclass of the ABC class, which stands for Abstract Base Class. It serves as a base class for other classes and can define abstract methods that must be implemented by its subclasses.
# The __init__ method is the constructor of the Database class. It takes a driver parameter, which represents the database driver. The self.driver attribute is set to the provided driver value.
# This connect_to_database method is marked as an abstract method using the @abstractmethod decorator. Subclasses of Database must implement this method, which should establish a connection to the specific database.
# The __enter__ method is a special method used in Python's context manager protocol. It is invoked when entering the context (using the with statement). Here, it establishes a database connection by calling the connect_to_database method and assigns the connection to self.connection. It also creates a cursor object (self.cursor) to execute SQL queries.
# The __enter__ method returns self, which allows you to use the instance of the Database class as a context manager within the with block.
# The __exit__ method is another special method used in the context manager protocol. It is called when exiting the context (leaving the with block). Here, it closes the cursor (self.cursor) and the database connection (self.connection).
# The __exit__ method receives three arguments: exception_type, exc_val, and traceback. These are used to handle any exceptions that occurred within the context. However, in our code, there is no explicit exception handling implemented.



class PgDatabase(Database):
    """PostgreSQL Database context manager"""
    def __init__(self) -> None:
        self.driver = psycopg2
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

# The PgDatabase class is defined as a subclass of the Database class. It specifically represents a PostgreSQL database context manager.
# The __init__ method initializes the PgDatabase object. It sets the self.driver attribute to psycopg2, which is the PostgreSQL driver library. Then, it calls the __init__ method of the parent Database class using super().__init__(self.driver), passing the psycopg2 driver as an argument.
# The connect_to_database method is implemented here to establish a connection to the PostgreSQL database using the psycopg2 driver. It retrieves the connection details from environment variables (os.getenv) such as DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, and DB_NAME. These environment variables should be set with the appropriate database configuration.
# The connect method of psycopg2 is called with the retrieved connection details to establish the connection. The method returns the connection object.
# Let’s create the .env file and add the followings(Please change the values by your credentials):


