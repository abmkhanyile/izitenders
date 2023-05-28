from .base_settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['tradeworld.herokuapp.com', 'www.tradeworld.co.za', 'leadshub.herokuapp.com', 'www.leadshub.co.za', '.localhost', 'localhost:5000']