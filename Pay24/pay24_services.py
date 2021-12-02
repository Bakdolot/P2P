from lxml import etree
from requests.structures import CaseInsensitiveDict
from .models import Category, Service

import re, os, json
import requests
import xmltodict


class Pay24ApiRequest:
    def __init__(self, login: str, password: str):
        self.base_url = 'https://test.pay24.asia/api2/xml/'
        self.login = login
        self.password = password

    @property
    def _get_category_xml(self):
        xml = etree.Element('request')
        etree.SubElement(xml, 'auth', attrib={'login': self.login, 'sign': self.password, 'signAlg': 'MD5'})
        providers = etree.SubElement(xml, 'providers')
        etree.SubElement(providers, 'getUIGroups')

        return etree.tostring(xml, xml_declaration=True, encoding='windows-1251')

    @property
    def _get_service_xml(self):
        xml = etree.Element('request')
        etree.SubElement(xml, 'auth', attrib={'login': self.login, 'sign': self.password, 'signAlg': 'MD5'})
        providers = etree.SubElement(xml, 'providers')
        etree.SubElement(providers, 'getUIProviders')

        return etree.tostring(xml, xml_declaration=True, encoding='windows-1251')

    @staticmethod
    def _check_categories(xml):
        try:
            resp_providers = xml.find('providers')
            resp_categories = resp_providers.find('getUIGroups')

            for sub_child in resp_categories.getchildren():
                if sub_child.getchildren():

                    try:
                        category = Category.objects.get(api_id=sub_child.get('id'))
                        category.name = sub_child.get('name')
                        category.logo_url = sub_child.get('logo')
                        category.save()

                    except Category.DoesNotExist:
                        category = Category.objects.create(
                            name=sub_child.get('name'),
                            api_id=sub_child.get('id'),
                            logo_url=sub_child.get('logo'),
                            order_id=sub_child.get('orderId')
                        )

            return True
        except Exception as e:
            return False

    @staticmethod
    def _check_services(xml):
        resp_providers = xml.find('providers')
        resp_services = resp_providers.find('getUIProviders')

        for child in resp_services:
            xml_bytes = etree.tostring(child, encoding='windows-1251')
            xml_to_json = xmltodict.parse(xml_bytes, encoding='windows-1251')
            data = json.dumps(xml_to_json, ensure_ascii=False)

            try:
                service = Service.objects.get(api_id=int(child.attrib['id']))
                service.logo_url = child.attrib['logo']
                service.min_sum = child.attrib['min_sum']
                service.max_sum = child.attrib['max_sum']
                service.support_phone = child.attrib['supportPhone']
                service.name = child.attrib['jName']
                service.data = data
            except:
                service = Service.objects.create(
                    category=int(child.attrib['grpId']),
                    api_id=int(child.attrib['id']),
                    logo_url=child.attrib['logo'],
                    order_id=child.attrib['orderId'],
                    min_sum=child.attrib['min_sum'],
                    max_sum=child.attrib['max_sum'],
                    support_phone=child.attrib['supportPhone'],
                    name=child.attrib['jName'],
                    commission='0',
                    data=data
                )
        return True

    def get_all_categories(self):
        url = f'{self.base_url}getUIGroups/'
        # send request to pay24 api
        response = requests.post(url, headers={'Content-Type': 'application/xml'},
                                 data=self._get_category_xml)
        resp_content = etree.XML(response.content)
        return self._check_categories(resp_content)

    def get_all_services(self):
        url = f'{self.base_url}getUIProviders/'
        # send request to pay24 api
        response = requests.post(url, headers={'Content-Type': 'application/xml'},
                                 data=self._get_service_xml)
        resp_content = etree.XML(response.content)
        return self._check_services(resp_content)


# test = Pay24ApiRequest('netex_api', '0265648a8056f0fd290f5ab619e8cd43b21fa68e79ab573b0fc5b881b4f5918t')
# test.get_all_categories()
