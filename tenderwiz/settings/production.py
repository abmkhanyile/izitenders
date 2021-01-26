from .base_settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['tradeworld.herokuapp.com', 'www.tradeworld.co.za', 'http://www.tradeworld.co.za', 'https://www.tradeworld.co.za', 'https://www.leadshub.co.za', '.localhost', 'localhost:5000']