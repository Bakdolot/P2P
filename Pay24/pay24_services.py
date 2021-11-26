from lxml import etree

import re, os


class Pay24ApiRequest:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    def get_all_categories(self):
        url = 'https://agent.asisnur.kg/api2/xml/getUIProviders/'
        
