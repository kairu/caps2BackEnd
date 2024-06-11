# DB Credentials (Temporary) will move to vault or env
class Config:
    DB_USER = 'avidatrack'
    DB_PASSWORD = 'password'
    DB_HOST = 'localhost'
    DB_PORT = '3306'
    DB_NAME = 'avida_track'
    SQLALCHEMY_DATABASE_URI = f'mariadb+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BULLETIN_IMAGES = 'static/bulletin-board'
    OCR_RECEIPTS = 'static/ocr-receipts'
    CONTRACTS = 'static/contracts'
    PAYMENT_IMAGES = 'static/payment-images'
    TEMP = 'static/TMP'
    SCHEDULER_API_ENABLED = True