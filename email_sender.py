#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: send_gmail.py
Description: this program deals with gmail sending
Creation: 2013-11-6
Revision: 2013-11-6
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import smtplib
import sys
import mimetypes
import email
#from email import MIMEMultipart
#from email import MIMEBase, MIMEText
#from email import MIMEAudio
#from email import MIMEImage
#from email import encode_base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


from getpass import getpass

def send_gmail(gmail_user=None, passwd=None, recipient=None, subject='', body='', attachmentFilePaths=tuple()):

    if not gmail_user or not recipient:
        raise AssertionError('Sorry, send_gmail is missing information.')

    passwd = passwd or getpass()

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    for attachmentFilePath in attachmentFilePaths:
        msg.attach(get_attachment(attachmentFilePath))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(gmail_user, passwd)
    s.sendmail(gmail_user, recipient, msg.as_string())
    s.close()

    print 'Sent email to %s' % recipient


def get_attachment(attachmentFilePath):
    contentType, encoding = mimetypes.guess_type(attachmentFilePath)

    if contentType is None or encoding is not None:
        contentType = 'application/octet-stream'

    mainType, subType = contentType.split('/', 1)

    with file(attachmentFilePath, 'rb') as f:
        if mainType == 'text':
            attachment = MIMEText(f.read())
        elif mainType == 'message':
            attachment = email.message_from_file(f)
        elif mainType == 'image':
            attachment = MIMEImage(f.read(),_subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(f.read(),_subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
        attachment.set_payload(f.read())
        #encode_base64(attachment)

    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachmentFilePath))
    return attachment

def send_btc(text_body):
    send_gmail(gmail_user='hendyhqq',
               passwd="hqq?1123581321",
               recipient='815515379@qq.com',
               subject='btc',
               body=text_body)

def send_tag_cloud(text_body):
    send_gmail(gmail_user='hendyhqq',
               passwd="hqq?1123581321",
               recipient='815515379@qq.com',
               subject='词云图',
               body=text_body)

if __name__ == "__main__":
    
    #===============================================================================
    # 接受参数
    #===============================================================================
    
#     text_body = sys.argv[1]
#     
#     send_gmail(gmail_user='hansolo19871217',
#                passwd="pi3.1415",
#                recipient='815515379@qq.com',
#                subject='cron output',
#                body=text_body)

    #===============================================================================
    # 接受stdin
    #===============================================================================
    
    text_body = sys.stdin.read()
    print text_body
    send_gmail(gmail_user='hansolo19871217',
                passwd="pi3.1415",
                recipient='815515379@qq.com',
                subject='cron output',
                body=text_body)
