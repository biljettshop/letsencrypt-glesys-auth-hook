#!/usr/bin/python3

import os
import sys
import requests

host = '.'.join(os.environ['CERTBOT_DOMAIN'].split('.')[:-2])
if host.startswith('*'):
	acme_host = '_acme_challenge' + host[1:]
else:
	acme_host = '_acme_challenge.' + host
domain = '.'.join(os.environ['CERTBOT_DOMAIN'].split('.')[-2:])

class GlesysRest(object):
    username = os.environ['GLESYS_USERNAME']
    api_key = os.environ['GLESYS_API_KEY']
    scheme = 'https://'
    base_url = 'api.glesys.com'
    format = 'json'

    def build_url(self, module, function):
        return "{scheme}{username}:{api_key}@{base_url}/{module}/{function}/format/{format}".format(
            scheme = self.scheme,
            username = self.username,
            api_key=self.api_key,
            base_url = self.base_url,
            module = module,
            function = function,
            format = self.format
        )

    def post(self, module, function, data={}, params={}, json=None):
        url = self.build_url(module, function)
        r = requests.post(url, data=data, params=params, json=json)
        return r

    def get(self, module, function, params={}):
        url = self.build_url(module, function)
        r = requests.get(url, params=params)
        return r

glesys = GlesysRest()

def auth():
	validation = os.environ['CERTBOT_VALIDATION']
	glesys.post('domain', 'addrecord', {
		'domainname': domain, 'host': acme_host, 'type': 'TXT', 'data': validation
	})

def cleanup():
	r = glesys.post('domain', 'listrecords', { 'domainname': domain })
	for record in r.json()['response']['records']:
		if record['host'] == acme_host and record['type'] == 'TXT':
			record_id = record['recordid']
			glesys.post('domain', 'deleterecord', {
                		'recordid': record_id
		        })
			break


if __name__ == "__main__":
	if sys.argv[1] == 'auth':
		auth()
	elif sys.argv[1] == 'cleanup':
		cleanup()
