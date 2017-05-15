#! /usr/bin/env python
# coding:utf-8
import top.api
import constants
def sms_captcha(sms_free_sign_name, rec_num, sms_temaplate_code, sms_param):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(constants.APPKEY, constants.SECRET))
    req.extend = ""
    req.sms_type = "normal"
    req.sms_free_sign_name = sms_free_sign_name
    req.sms_param = {'captcha':sms_param}
    req.rec_num = rec_num.decode('utf-8').encode('ascii')
    req.sms_template_code = sms_temaplate_code
    try:
        resp = req.getResponse()
        print (resp)
        return True
    except Exception, e:
        print (e)
        return False