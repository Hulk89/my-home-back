import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I_have_a_great_secret!'
