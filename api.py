
import requests
import json
from time import sleep

class WalmartAPI(object):

    def __init__(self, api_key, linkshare_id=None):

        self.api_key = api_key
        self.linkshare_id = linkshare_id

    def lookup_upc(self, upc):
        return self._request('upc', upc)


    def lookup_id(self, walmart_id):
        return self._request('itemId', walmart_id)

    def lookup_batch(self, ids):
        return self._request('ids', ','.join(ids))


    def _request(self, param_name, param):
        url = 'http://api.walmartlabs.com/v1/items'

        payload = {'apiKey': self.api_key, 'format': 'json', param_name: param}

        if self.linkshare_id:
            payload['lsPublisherId'] = self.linkshare_id


        r = requests.get(url, params=payload)
        print r.url
        sleep(0.5)

        try:
            j = r.json()
        except Exception as e:
            import traceback
            print traceback.format_exc()
            return

        try:

            for item in j['items']:
                yield WalmartProduct(data=item)

        except KeyError:
            print 'Walmart error'
        except IndexError:
            print 'Walmart error'


class WalmartProduct(object):

    def __init__(self, data):
        self.data = data

    @property
    def itemId(self):
        return self.__safe_get_value('itemId')

    @property
    def name(self):
        return self.__safe_get_value('name')

    @property
    def price(self):
        return self.__safe_get_value('salePrice')

    @property
    def upc(self):
        return self.__safe_get_value('upc')

    @property
    def large_image(self):
        return self.__safe_get_value('largeImage')

    @property
    def url(self):
        return self.__safe_get_value('productTrackingUrl')

    @property
    def is_marketplace(self):
        return self.__safe_get_value('marketplace')

    @property
    def is_available_online(self):
        return self.__safe_get_value('availableOnline')

    @property
    def shipping_cost(self):
        return self.__safe_get_value('standardShipRate')

    def __safe_get_value(self, key):
        try:
            return self.data[key]
        except KeyError:
            print 'WalmartError: did not find {0}'.format(key)

