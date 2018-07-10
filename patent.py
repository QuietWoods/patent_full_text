# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 18:53
# @Author  : QuietWoods
# @FileName: patent.py
# @Software: PyCharm
# @Email    ：1258481281@qq.com
# -*- coding: utf-8 -*-
import json
import re
import os
import time
import logging
import sys

from bs4 import BeautifulSoup
import requests
import url_config
from url_config import PATENT_NUMBER_SET, PATENT_TEXT_DIR

from controller.mylog import logger
from service.account import *


class PatentNumber:
    """
    专利申请号集，避免重复下载
    """
    # 申请号集
    request_nmuber_dict = []
    # 专利完成下载集合
    have_download_set = set()

    def __init__(self):
        # 打开专利原文的申请号集合，根据申请号来检索对应的专利。
        with open(PATENT_NUMBER_SET, 'r', encoding='utf-8') as f:
            for line in f:
                count, patent_number = line.strip().split('\t')
                self.request_nmuber_dict.append(patent_number)

        # 打开下载目录，收集已经下载好的专利。
        for fname in os.listdir(PATENT_TEXT_DIR):
            key = fname.split('.')[0]
            self.have_download_set.add(key)


class PatentSpider:
    """
    专利全文爬虫
    """
    patent_num = PatentNumber()
    sipoList = patent_num.request_nmuber_dict
    down_set = patent_num.have_download_set
    cookies = None
    deal_with_cookies = 0  # 统计cookies的输入次数
    cookies_time = 0  # 时间戳，记录输入cookies时间点

    def parse_cookie_str(self, cookie_str):
        """
        解析cookies
        :param cookie_str:
        :return:
        """
        cookie_dict = {}
        items = cookie_str.strip().split(';')
        for item in items:
            key, value = item.strip().split('=')
            cookie_dict[key] = value
        return cookie_dict

    def componet_search(self, patent_number):
        """
        组建检索表达式
        :param patent_number:
        :return:
        """
        return "申请号=(" + patent_number + "+)"

    def get_cookies(self):
        login_ok = False
        if ctrl.BEING_LOG is False:
            login_ok = login()
        if login_ok:
            self.cookies = ctrl.COOKIES
        else:
            while not login_ok:
                time.sleep(30 * 60 * 60)
                login_ok = login()
            self.cookies = ctrl.COOKIES
            # cookie_str = input("初始化cookie值:")
            # self.cookies = self.parse_cookie_str(cookie_str)

        self.deal_with_cookies += 1
        now_time = time.time()
        # 计算时间间隔
        interval = now_time - self.cookies_time
        # 更新时间点
        self.cookies_time = time.time()
        if self.deal_with_cookies == 1:
            interval = 0
        logger.info('第{}次,输入cookies值，间隔时间：{:.1f} 秒, {}'.format(self.deal_with_cookies, interval, self.cookies))

    # 初始化高级检索表
    def start_requests(self):
        mainSearch = url_config.mainSearch
        headers = mainSearch.get('headers')
        # cookie_str = input("请输入cookie值进行初始化:")
        # cookies = self.parse_cookie_str(cookie_str)
        # self.cookies = self.get_cookies()
        self.get_cookies()
        # 专利全文
        patent_item = {}
        for count, request_number in enumerate(self.sipoList):
            count += 1
            if request_number in self.down_set:
                logger.info('{}已经存在，跳过下载'.format(request_number))
                continue
            
            patent_item['request_number'] = request_number
            # searchExpCn = "申请号=(CN201410811795+)"
            searchExpCn = self.componet_search(request_number)
            logger.info('第{}个检索表达式--- {}'.format(count, searchExpCn))
            form_data = mainSearch.get('form_data')
            form_data.__setitem__('searchCondition.searchExp', searchExpCn)
            # 检索patent_id
            first_response = requests.post(
                url=url_config.mainSearch.get('url'),
                headers=headers,
                cookies=self.cookies,
                data=form_data
            )
            # 抽取patent_id
            patent_id = self.parseFirstPage(first_response)
            if not patent_id:
                logger.error('patent_id is {}'.format(patent_id))
                self.get_cookies()  # 更新一次cookies，当前专利记录不完整，放弃当前记录，进行下一条。
                continue
            # 专利ID
            patent_item['patent_id'] = patent_id
            # 组建标题和摘要的表单
            form_data = url_config.detailSearch.get('form_data')
            form_data.__setitem__('nrdAn', str(patent_id).split('.')[0])
            form_data.__setitem__('cid', str(patent_id))
            form_data.__setitem__('sid', str(patent_id))
            logger.info('获取专利ID：{}\n'.format(patent_id))
            # print(form_data)
            # 检索摘要和标题
            abstract_title_response = requests.post(
                url=url_config.detailSearch.get('url'),
                headers=url_config.detailSearch.get('headers'),
                cookies=self.cookies,
                data=form_data
            )
            # 解析摘要和标题
            abstract, title = self.parsePatentDetail(abstract_title_response)
            if not abstract and not title:
                logger.error('abstract is {}, title is {}'.format(abstract, title))
                self.get_cookies()  # 更新一次cookies，当前专利记录不完整，放弃当前记录，进行下一条。
                continue
            patent_item['abstract'] = abstract
            patent_item['title'] = title
            
            # 组建权利要求和说明书表单
            form_data = url_config.full_text.get('form_data')
            form_data.__setitem__('nrdAn', str(patent_id).split('.')[0])
            form_data.__setitem__('cid', str(patent_id))
            form_data.__setitem__('sid', str(patent_id))
            # 检索权利要求和说明书
            full_text_response = requests.post(
                url=url_config.full_text.get('url'),
                headers=url_config.full_text.get('headers'),
                cookies=self.cookies,
                data=form_data
            )
            # 解析权利要求和说明书
            claim, instructions = self.parse_full_text(full_text_response)
            if not claim and not instructions:
                logger.error('claim is {}, instructions is {}'.format(claim, instructions))
                self.get_cookies()  # 更新一次cookies，当前专利记录不完整，放弃当前记录，进行下一条。
                continue
            patent_item['claim'] = claim
            patent_item['instructions'] = instructions
            # 写入到本地
            self.write_patent_item(count, patent_item)

    # 解析检索回来的json文件
    def _parse_basic(self, record_list):
        if not record_list:
            return None
        result = []
        try:
            for record in record_list:
                basic = {}
                basic['nrdAn'] = record.get('fieldMap').get('AP')
                basic['nrdPn'] = record.get('fieldMap').get('PN')
                basic['patent_id'] = record.get('fieldMap').get('ID')
                basic['request_number'] = record.get('fieldMap').get('APO')
                basic['request_date'] = record.get('fieldMap').get('APD')
                basic['publish_number'] = record.get('fieldMap').get('PN')
                basic['publish_date'] = record.get('fieldMap').get('PD')
                basic['invention_name'] = record.get('fieldMap').get('TIVIEW')
                basic['inventor'] = record.get('fieldMap').get('INVIEW')
                basic['proposer'] = record.get('fieldMap').get('PAVIEW')
                basic['agent'] = record.get('fieldMap').get('AGT')
                basic['agency'] = record.get('fieldMap').get('AGY')
                # 去除<FONT>和</FONT>格式
                for key, value in basic.items():
                    basic[key] = re.sub(r'</{0,1}FONT>', '', value)
                result.append(basic)
            return result
        except Exception as e:
            logger.error(e)
            return None

    # 解析第一页专利组
    def parseFirstPage(self, response):
        if response.status_code == 200:
            try:
                result = json.loads(response.text)
                searchResultRecord = result['searchResultDTO']['searchResultRecord']
                if searchResultRecord:
                    result_list = self._parse_basic(searchResultRecord)
                    if len(result_list) > 0:
                        # 只取第一项
                        item = result_list[0]
                        patentid = item.get('patent_id')
                        return patentid
                    else:
                        logger.info('无记录！')
                        return None
                else:
                    logger.error('检索列表出错了！')
                    return None
            except Exception as e:
                logger.error('{},\n{}'.format(response.text, response.headers))
                logger.error(e)
                return None
        else:
            return None

    # 解析专利详情，标题和摘要
    def parsePatentDetail(self, response):
        # print(response.text)
        print(response.status_code)
        if response.status_code == 200:
            # print(response.text)
            # print('-----------------------')
            # print(response.content)
            try:
                detail = json.loads(response.text)
                abstract = BeautifulSoup(detail.get('abstractInfoDTO').get('abIndexList')[0].get('value'),
                                         'lxml').text.replace('\n', '').strip()
                invention_name = detail.get('abstractInfoDTO').get('tioIndex').get('value')
                return abstract, invention_name
            except Exception as e:
                logger.error('{},\n{}'.format(response.text, response.headers))
                logger.error(e)
                return None, None
        else:
            logger.error('解析专利标题和摘要出错！')
            return None, None

    # 解析专利权利要求书和说明书
    def parse_full_text(self, response):
        if response.status_code == 200:
            try:
                full_text = json.loads(response.text)
                full_text_dto = full_text.get('fullTextDTO')
                clain_instruct_str = full_text_dto['literaInfohtml']
                clain, instruction = self.clear_claim(clain_instruct_str)
                return clain, instruction
            except Exception as e:
                logger.error('{},\n{}'.format(response.text, response.headers))
                logger.error(e)
        else:
            return None, None

    def clear_claim(self, claim_instru):
        '''清洗权利要求书和说明书，并拆开'''
        if not claim_instru:
            return None, None
        split_list = claim_instru.split(u'</div>')
        if len(split_list) < 2:
            return None, None
        claim, instructions = split_list[0], split_list[1]
        # 正则表达式去除有效（无效）的html标签
        dr = re.compile(r'</?[^>]+>', re.S)
        claim = dr.sub('', claim)
        instructions = dr.sub('', instructions)
        # 去除任意空白字符
        dr = re.compile(r'\s+', re.S)
        claim = dr.sub('', claim)
        instructions = dr.sub('', instructions)
        # print('cliam: ', claim)
        # print('instru: ', instructions)
        return claim[5:], instructions[3:]

    # 根据标点符号切割段落
    def segment_by_punctuation(string):
        if not string:
            return None
        split_list = string.split(u'。')
        result = ''
        for seg in split_list:
            result += seg + '\n'
        return result

    def write_patent_item(self, count, patent_item):
        """
        写入 标题，摘要，权利要求书，说明书
        :param count:
        :param patent_item:
        :return:
        """
        if patent_item:
            # 拼接专利全文的路径
            patent_path = os.path.join(PATENT_TEXT_DIR, patent_item['request_number'] + '.txt')
            with open(patent_path, 'w', encoding='utf-8') as w:
                w.write("{}\n{}\n{}\n{}".format(patent_item['title'],
                                                patent_item['abstract'],
                                                patent_item['claim'],
                                                patent_item['instructions']))
            logger.info('第{}篇专利全文写入{} 完成!'.format(count, patent_path))
        else:
            logger.error('专利全文写到本地失败！')


if __name__ == '__main__':
    patent_spider = PatentSpider()
    logger.info('爬取专利全文开始...')
    patent_spider.start_requests()
