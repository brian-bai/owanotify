#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
from selenium import webdriver
import pandas as pd
import subprocess
import configparser

def sendmessage(title, message):
    subprocess.Popen(['notify-send', title, message])
    return

def getconfig():
    OWA_CONFIG = 'data/owa.ini'
    config = configparser.ConfigParser()
    config.read(OWA_CONFIG)
    return(config)

def getMails(config):
    driver = webdriver.Chrome(config['OWA']['driver_path'])
    driver.get(config['OWA']['owaurl'])
    time.sleep(1)
    driver.find_element_by_id('username').send_keys(config['OWA']['username'])
    driver.find_element_by_id('password').send_keys(config['OWA']['password'])
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

def processMail(config,mails):
    old_mail = pd.read_csv(config['OWA']['old_mail_csv'], index_col=0)
    newmails = mails[~mails['receive'].isin(old_mail['receive'])]
    if len(newmails)>0:
        newmails.to_csv(config['OWA']['new_mail_csv'])
        mails.to_csv(config['OWA']['old_mail_csv'])
        sendmessage("Mails Notification", "There are %d new mails"%len(newmails))
        for i in newmails.index:
            mail = newmails.iloc[i]
            sendmessage(mail['subject'], mail['from'] + ' ' + mail['receive'] )
    else:
        sendmessage("Mails notification",'No new email!')

if __name__ == '__main__':
    config = getconfig()
    mails = getMails(config)
    processMail(config, mails)
