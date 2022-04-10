from .base_settings import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'j0fyf510lvqlmj&4fhhhcl=9=(c3f6_&n3pt0h!sso6f4@h5k#')

DEBUG = False

ALLOWED_HOSTS = ['tradeworld.herokuapp.com', 'www.tradeworld.co.za', 'http://www.tradeworld.co.za', 'https://www.tradeworld.co.za', 'https://www.leadshub.co.za', 'http://www.leadshub.co.za', 'http://leadshub.co.za', 'leadshub.herokuapp.com', '.localhost', 'localhost:5000']