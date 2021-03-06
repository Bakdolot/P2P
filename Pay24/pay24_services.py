from lxml import etree

from .models import Category, Service
from internal_transfer.services import create_operation

import json
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

    def _get_payment_xml(self, payment):
        xml = etree.Element('request')
        etree.SubElement(xml, 'auth', attrib={'login': self.login, 'sign': self.password, 'signAlg': 'MD5'})
        providers = etree.SubElement(xml, 'providers')
        add_payment_offline = etree.SubElement(providers, 'addOfflinePayment')
        payment_id = etree.SubElement(add_payment_offline, 'payment', attrib={'id': payment.id})
        body = etree.SubElement(payment_id, 'to', attrib={
            'service': payment.service,
            'account': payment.account,
            'amount': payment.amount,
            'currency': '417',
        })

        return xml

    @staticmethod
    def _delete_non_active_instance(queryset, lst: list):  # TODO: why it work that?
        for i in queryset:
            if i.api_id in lst:
                i.delete()
        return True

    def _check_categories(self, xml):
        resp_providers = xml.find('providers')
        resp_categories = resp_providers.find('getUIGroups')

        api_ids = []
        for sub_child in resp_categories.getchildren():
            if sub_child.getchildren():
                api_ids.append(sub_child.get('id'))
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

        self._delete_non_active_instance(Category.objects.all(), api_ids)
        return True

    def _check_services(self, xml):
        resp_providers = xml.find('providers')
        resp_services = resp_providers.find('getUIProviders')

        api_ids = []
        for child in resp_services:
            xml_bytes = etree.tostring(child, encoding='windows-1251')
            xml_to_json = xmltodict.parse(xml_bytes, encoding='windows-1251')
            data = json.dumps(xml_to_json, ensure_ascii=False)
            api_ids.append(child.attrib['id'])
            try:
                service = Service.objects.get(api_id=int(child.attrib['id']))
                service.logo_url = child.attrib['logo']
                service.min_sum = child.attrib['min_sum']
                service.max_sum = child.attrib['max_sum']
                service.support_phone = child.attrib['supportPhone']
                service.name = child.attrib['jName']
                service.data = data
            except:
                Service.objects.create(
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

        self._delete_non_active_instance(Service.objects.all(), api_ids)
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

    def add_payment(self, payment):
        url = f'{self.base_url}addOfflinePayment/'
        payment = self._get_payment_xml(payment)
        response = requests.post(url, headers={'Content-Type': 'application/xml'}, data=payment)

        return response
