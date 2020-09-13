import configparser

settings = configparser.ConfigParser()

settings.read('settings.ini', encoding='utf-8')

user = settings['HOGEHOGE']['User']

oanda_token = settings['oanda']['token']
oanda_id = settings['oanda']['id']





