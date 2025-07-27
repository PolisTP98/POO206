from datetime import timedelta

class Config:
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_DB = "dbflask"
    SECRET_KEY = "mysecretkey"
    PERMANENT_SESSION_LIFETIME = timedelta(0)