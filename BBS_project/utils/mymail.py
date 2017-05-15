#! /usr/bin/env python
# coding:utf-8

from flask_mail import Message
from exts import mail



def send_mail(receivers,subject,body=None,html=None):
    if not body and not html:
        return False
    # receivers:可以传字符串或list
    # 如果是字符串就包裹成list 再传入
    if isinstance(receivers,str) or isinstance(receivers,unicode):
        receivers = [receivers]
    msg = Message(subject=subject,recipients=receivers,body=body,html=html)
    try:
        mail.send(msg)
    except:
        return False
    return True