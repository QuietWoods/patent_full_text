import base64
import requests

import controller as ctrl
from setting import CAPTCHA_MODEL_NAME, TIMEOUT, USE_PROXY
from url_config import url_captcha, url_login
from service.proxy import update_proxy, notify_ip_address, update_cookies
from service.sipoknn import get_captcha_result
from controller.mylog import logger


account_notify_times = 0
description = (
    '''
    用户信息配置模块

    由于专利网站的改版，现在要求必须要登录账号密码才能进行高级查询，
    请使用者到专利网站自行注册账号，并修改一下USERNAME和PASSWORD的值
    链接：http://www.pss-system.gov.cn/sipopublicsearch/portal/uiregister-showRegisterPage.shtml
    '''
)


class Account:
    """
    账户信息定义
    """

    def __init__(self):
        # 用户名，约定私有约束，使用请调用self.username
        self._username = '********'
        # 密码，约定私有约束，使用请调用self.password
        self._password = '********'

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


# 账户信息的单例
account = Account()


def change_to_base64(source):
    """
    将参数进行base64加密
    :param source:
    :return:
    """
    return str(base64.b64encode(bytes(source, encoding='utf-8')), 'utf-8')


def get_captcha():
    """
    获取验证码
    :return:
    """
    resp = requests.get(url=url_captcha.get('url'), cookies=ctrl.COOKIES)
    with open('captcha.png', 'wb') as f:
        f.write(resp.content)
    result = get_captcha_result(CAPTCHA_MODEL_NAME, 'captcha.png')
    return result


def check_login_status():
    if USE_PROXY:
        try:
            if ctrl.PROXIES is not None:
                notify_ip_address()
                logger.info('当前已有登录状态')
                return True
        except:
            pass
    return False


def login(username=None, password=None):
    """
    登录API
    :return: True: 登录成功; False: 登录失败
    """
    if username is None or password is None:
        username = account.username
        password = account.password
    ctrl.BEING_LOG = True
    if check_login_status():
        ctrl.BEING_LOG = False
        return True

    error_times = 0
    while True:
        try:
            update_proxy()
            update_cookies()
            busername = change_to_base64(username)
            bpassword = change_to_base64(password)
            captcha = get_captcha()
            logger.info('验证码识别结果：%s' % captcha)
            form_data = url_login.get('form_data')
            form_data.__setitem__('j_validation_code', captcha)
            form_data.__setitem__('j_username', busername)
            form_data.__setitem__('j_password', bpassword)

            resp = requests.post(url=url_login.get('url'), headers=url_login.get('headers'), data=form_data,
                                 cookies=ctrl.COOKIES, proxies=ctrl.PROXIES, timeout=TIMEOUT)
            if resp.text.find(username + '，欢迎访问') != -1:
                jsession = ctrl.COOKIES.get('JSESSIONID')
                resp.cookies.__delitem__('JSESSIONID')
                resp.cookies.set('JSESSIONID', jsession, domain='www.pss-system.gov.cn')
                update_cookies(resp.cookies)
                requests.post(
                    'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml',
                    cookies=ctrl.COOKIES, proxies=ctrl.PROXIES)
                ctrl.BEING_LOG = False
                logger.info('登录成功')
                return True
            else:
                if error_times > 5:
                    break
                logger.error('登录失败')
                error_times += 1
        except Exception as e:
            logger.error(e)

    ctrl.BEING_LOG = False
    return False

