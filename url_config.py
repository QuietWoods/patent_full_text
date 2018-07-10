# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 20:14
# @Author  : QuietWoods
# @FileName: url_config.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
import requests

url_index = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
    'headers': {}
}

# 预处理地址，主要的目的是把ip发送给对面
url_pre_execute = {
    # 'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/preExecuteSearch!preExecuteSearch.do',
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/pageIsUesd-pageUsed.shtml',
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://www.pss-system.gov.cn",
        "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml",
        "X-Requested-With": "XMLHttpRequest"
    }
}
# 主查询地址
# 这个地址经常改变
mainSearch = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0529-executeCommandSearch.shtml',

    'headers': {
        "Host": "www.pss-system.gov.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    },
    'form_data': {
        "searchCondition.searchExp": '',
        "searchCondition.dbId": "VDB",
        "searchCondition.searchType": "Sino_foreign",
        "searchCondition.extendInfo['MODE']": "MODE_TABLE",
        "searchCondition.extendInfo['STRATEGY']": "STRATEGY_CALCULATE",
        "searchCondition.originalLanguage": "",
        "searchCondition.targetLanguage": "",
        "wee.bizlog.modulelevel": "0200201",
        "resultPagination.limit": '12'
    }
}

# 查询专利摘要的地址
detailSearch = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/viewAbstractInfo0529-viewAbstractInfo.shtml',
    'headers': {
        "Host": "www.pss-system.gov.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    },
    'form_data': {
        'nrdAn': '',
        'cid': '',
        'sid': '',
        'wee.bizlog.modulelevel': '0201101'
    }
}

# 专利全文
full_text = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showFullText0529-viewFullText.shtml',
    'headers': {
        "Host": "www.pss-system.gov.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    },
    'form_data': {
        'nrdAn': '',
        'cid': '',
        'sid': '',
        'wee.bizlog.modulelevel': '0201103'
    }
}
# 验证码地址
url_captcha = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml',
    'headers': {}
}

# 登录地址
url_login = {
    'url': 'http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check',
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Host': 'www.pss-system.gov.cn',
        'Origin': 'http://www.pss-system.gov.cn',
        'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    },
    'form_data': {
        "j_loginsuccess_url": "",
        "j_validation_code": '',
        "j_username": '',
        "j_password": ''
    }
}
# 药类专利原文目录，文本格式
PATENT_TEXT_DIR = "G:\\data\\patent\\tmp\\text"
# PATENT_TEXT_DIR = "patent_text"
# 专利号集
PATENT_NUMBER_SET = "patent_number\\PDF原文集.txt"


if __name__ == '__main__':
    resp = requests.get(url_index.get('url'), headers=mainSearch.get('headers'))
    coo = resp.cookies
    print(coo)
    coo.__delitem__('JSESSIONID')
    coo.set('JSESSIONID', '8U9nCtA0LoRYs75ado1-eMcbTsLZINYi2r3aILoqbKjmy9DbWY_v!891074563!-395222046',
            domain='www.pss-system.gov.cn')
    coo.__delitem__('IS_LOGIN')
    coo.set('IS_LOGIN', 'true', domain='www.pss-system.gov.cn/sipopublicsearch/patentsearch')
    coo.__delitem__("WEE_SID")
    coo.set("WEE_SID", '8U9nCtA0LoRYs75ado1-eMcbTsLZINYi2r3aILoqbKjmy9DbWY_v!891074563!-395222046!1522147184692',
            domain='www.pss-system.gov.cn/sipopublicsearch/patentsearch')
    print(coo)
    form_data = detailSearch.get('form_data')
    # '''
    # 'nrdAn': '',
    #     'cid': '',
    #     'sid': '',
    #     'wee.bizlog.modulelevel': '0201101'
    # '''
    form_data.__setitem__('nrdAn', 'CN201711283836')
    form_data.__setitem__('cid', 'CN201711283836.720180302FM')
    form_data.__setitem__('sid', 'CN201711283836.720180302FM')
    resp = requests.post(detailSearch.get('url'), headers=detailSearch.get('headers'), cookies=coo, data=form_data)
    print(resp.text)
    pass
    # search_exp_cn = QUERY_LIST[0].search_exp_cn
    # form_data = url_search.get('formdata')
    # form_data.__setitem__('searchCondition.searchExp', search_exp_cn)

    # print(resp.content.decode())