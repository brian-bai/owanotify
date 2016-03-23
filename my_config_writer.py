import configparser
'''use this script to generate the config file
   then copy to data folder'''
config = configparser.ConfigParser()
config['OWA'] = {'DRIVER_PATH':'/home/brian/Downloads/chromedriver',
                  'OWAURL':'https://webmail.xxxxx.com',
                  'USERNAME':r'xxxCORP\xxxx.xxx',
                  'PASSWORD': "xxxxxxx",
                  'NEW_MAIL_CSV': "data/mails_new.csv",
                  'OLD_MAIL_CSV': "data/mails_old.csv"}

with open('owa.ini', 'w') as configfile:
    config.write(configfile)
