#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
from selenium import webdriver
import pandas as pd
import subprocess
import configparser
import logging

class MailChecker(object):
    def __init__(self):
        self.config = {}

    def sendmessage(self, title, message):
        subprocess.Popen(['notify-send', title, message])
        return
    
    def getconfig(self):
        OWA_CONFIG = 'data/owa.ini'
        config = configparser.ConfigParser()
        config.read(OWA_CONFIG)
        self.config = config['OWA']
    
    def getMails(self):
        driver = webdriver.Chrome(self.config['driver_path'])
        driver.get(self.config['owaurl'])
        time.sleep(1)
        driver.find_element_by_id('username').send_keys(self.config['username'])
        driver.find_element_by_id('password').send_keys(self.config['password'])
        driver.find_element_by_id('SubmitCreds').click()
        time.sleep(1)
        content = driver.find_elements_by_css_selector("div.cntnt")
        froms = content[0].find_elements_by_xpath(".//td[5]")
        subjects = content[0].find_elements_by_xpath(".//td[6]")
        receives = content[0].find_elements_by_xpath(".//td[7]")
        sizes = content[0].find_elements_by_xpath(".//td[8]")
        mails = pd.DataFrame({'from': [f.text for f in froms], 'subject': [ s.text for s in subjects], 'receive':[r.text for r in receives], 'size':[s.text for s in sizes]})
        driver.quit()
        return(mails)
    
    def processMail(self,mails):
        old_mail = pd.read_csv(self.config['old_mail_csv'], index_col=0)
        newmails = mails[~mails['receive'].isin(old_mail['receive'])]
        if len(newmails)>0:
            newmails.to_csv(self.config['new_mail_csv'])
            mails.to_csv(self.config['old_mail_csv'])
            self.sendmessage("Mails Notification", "There are %d new mails"%len(newmails))
            for i in newmails.index:
                mail = newmails.iloc[i]
                self.sendmessage(mail['subject'], mail['from'] + ' ' + mail['receive'] )
        else:
            self.sendmessage("Mails notification",'No new email!')
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
          format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s %(message)s',
          datefmt='%a, %d %b %Y %H:%M:%S',
          filename='mailchecker.log',
          filemode='w')
            
    mailChecker = MailChecker()
    mailChecker.getconfig()
    mails = mailChecker.getMails()
    logging.info("Retrieved %d mails"%len(mails))
    mailChecker.processMail(mails)
