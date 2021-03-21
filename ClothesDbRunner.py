from bottle import run
from ClothesWebConfig import AppConfig
from ClothesWebApp import app

appconfig = AppConfig()
app.config['db'] = appconfig.db

if __name__ == '__main__':
    run(host=appconfig.hostname, port=appconfig.port)
