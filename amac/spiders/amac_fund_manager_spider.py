#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import json
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class AmacManagerSpider(scrapy.Spider):
    name = "amac_manager"

    def start_requests(self):
        urls = [
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754044&page=1&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754045&page=2&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754046&page=3&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754047&page=4&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754048&page=5&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754049&page=6&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754050&page=7&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754051&page=8&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754052&page=9&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754053&page=10&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754054&page=11&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754055&page=12&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754056&page=13&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754057&page=14&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754058&page=15&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754059&page=16&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754060&page=17&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754061&page=18&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754062&page=19&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754063&page=20&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754064&page=21&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754065&page=22&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754066&page=23&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754067&page=24&size=1000',
            'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.41772204142754068&page=25&size=1000'
        ]
        for url in urls:
            yield scrapy.Request(url=url, method='POST', callback=self.parse,
                                 headers={'content-type': 'application/json'}, body='{}')

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for item in jsonresponse['content']:
            detail_html = item['url']
            if (detail_html):
                manager_detail_url = '/amac-infodisc/res/pof/manager/' + item['url']
                yield response.follow(manager_detail_url, callback=self.parse_manager_detail,
                                      meta={'item': item})
            else:
                item['fund_official_url'] = None
                yield item

    def parse_manager_detail(self, response):
        item = response.meta['item']
        fund_official_url = response.xpath(
            '/html/body/div/div[2]/div/table/tbody/tr[13]/td[4]/a/text()').extract_first()
        if fund_official_url:
            if 'http' not in fund_official_url:
                fund_official_url = 'http://' + fund_official_url
            item['fund_official_url'] = fund_official_url
            yield item
        else:
            item['fund_official_url'] = None
            yield item
