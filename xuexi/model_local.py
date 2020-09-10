#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
from xuexi.unit import cfg, logger


class Structure:
    _fields = []

    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Set all of the positional arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Set the remaining keyword arguments
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        # Check for any remaining unknown arguments
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))


class Bank(Structure):
    _fields = ['id', 'category', 'content', 'options', 'answer', 'excludes', 'description']

    def __repr__(self):
        return f'{self.content}'

    def to_json(self):
        pass

    @classmethod
    def from_json(self, data):
        pass


class BankQuery:
    def __init__(self):
        self.dataKu = cfg.get('api', 'datajson')

    def post(self, item, dataFile=None):
        if not dataFile:
            dataFile = self.dataKu
        # if "" == item["content"]:
        #     logger.debug(f'content is empty')
        with open(dataFile, 'r', encoding='utf8') as f:
            dataKu = json.load(f)
        print(dataKu)

    def put(self, item, url=None):
        if not url:
            url = self.url
        if "" == item["content"]:
            logger.debug(f'content is empty')
            return False
        logger.debug(f'PUT {item["content"]} {item["options"]} {item["answer"]} {item["excludes"]}...')
        try:
            res = requests.put(url=url, headers=self.headers, json=item)
            if 201 == res.status_code:
                logger.info('添加新记录')
                return True
            elif 200 == res.status_code:
                logger.info('更新记录')
                return True
            else:
                logger.debug("PUT do nothing")
                return False
        except:
            return False

    def get(self, item, url=None):
        if not url:
            url = self.url
        if "" == item["content"]:
            logger.debug(f'content is empty')
            return None
        logger.debug(f'GET {item["content"]}...')
        try:
            res = requests.post(url=url, headers=self.headers, json=item)
            if 200 == res.status_code:
                logger.debug(f'GET item success')
                # logger.debug(res.text)
                # logger.debug(json.loads(res.text))
                return json.loads(res.text)
            else:
                logger.debug(f'GET item failure')
                return None
        except:
            logger.debug('request faild')
            return None