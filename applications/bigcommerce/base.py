# -*- coding: utf-8 -*-
"""
    BigCommerce API Reference
    @BigCommerceModel
        include base func:
            get_method
            delete_method
            post_method
            put_method
"""
import requests
from django.conf import settings


class BigCommerceModel:
    """
        BigCommerceModel
    """

    def __init__(self, logger):
        """
        init data: logger endpoint
        :param logger:
        """
        self.logger = logger
        self.endpoint = 'https://api.bigcommerce.com/stores'

    @staticmethod
    def get_headers(store_hash: str):
        """
            @get_headers
        :return: self.headers
        """
        access_token = list(filter(lambda x: x.get("store_hash") == store_hash, settings.APP_CLIENTS.values()))

        if any(access_token) is False:
            raise Exception("parser access token error")

        access_token = access_token[0].get("access_token")

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Auth-Client": access_token,
            "X-Auth-Token": access_token
        }

    def get_method(self, store_hash, uri, params=None, version='v3'):
        """
            @get_method
        :param store_hash: store code
        :param uri: requests url
        :param params: get methods params
        :param version: bc api version
        :return: status_code, result
        """
        url = "{0}/{1}/{2}".format(self.endpoint, store_hash, version) + uri
        resp = requests.get(url, headers=self.get_headers(store_hash), params=params)
        self.logger.info("url:{url}, status_code:{status_code}".format(
            url=resp.url, status_code=resp.status_code))
        if resp.status_code == 200:
            result = resp.json()
        else:
            result = False
        return result

    def delete_method(self, store_hash, uri, params=None, version='v3'):
        """
            @delete_method
        :param store_hash: store code
        :param uri: requests url
        :param params: delete methods params
        :param version: bc api version
        :return: status_code result
        """
        url = "{0}/{1}/{2}".format(self.endpoint, store_hash, version) + uri
        resp = requests.delete(url, headers=self.get_headers(store_hash), params=params)
        self.logger.info("url:{url}, status_code:{status_code}".format(
            url=resp.url, status_code=resp.status_code))
        if resp.status_code == 200:
            result = resp.json()
        else:
            result = False
        return result

    def post_method(self, store_hash, uri, data, version='v3'):
        """
            @post_method
        :param store_hash: store code
        :param uri: requests url
        :param data: post methods data
        :param version: bc api version
        :return: status_code result
        """
        url = "{0}/{1}/{2}".format(self.endpoint, store_hash, version) + uri
        resp = requests.post(url, headers=self.get_headers(store_hash), data=data)
        self.logger.info("url:{url}, status_code:{status_code}".format(
            url=resp.url, status_code=resp.status_code))
        if resp.status_code == 200 or resp.status_code == 201:
            result = resp.json()
        else:
            result = False
        return result

    def put_method(self, store_hash, uri, data, version='v3'):
        """
            @put_method
        :param store_hash: store code
        :param uri: requests url
        :param data: put methods data
        :param version: bc api version
        :return: status_code result
        """
        url = "{0}/{1}/{2}".format(self.endpoint, store_hash, version) + uri
        resp = requests.put(url, headers=self.get_headers(store_hash), data=data)
        self.logger.info("url:{url}, status_code:{status_code}".format(
            url=resp.url, status_code=resp.status_code))
        if resp.status_code == 200 or resp.status_code == 201:
            result = resp.json()
        else:
            result = False
        return result
