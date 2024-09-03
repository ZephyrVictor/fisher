# encoding=utf-8
__author__ = 'Zephyr369'
import requests

class HTTP:
    @staticmethod
    def get(url, return_json=True):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            'Referer':'https://some.trusted.source.com/'
        }

        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
