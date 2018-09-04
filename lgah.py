#!/bin/python3

import sys

host = '_acme_challenge.' + '.'.join(sys.environ['CERTBOT_DOMAIN'].split('.')[:-2])
domain = '.'.join(sys.environ['CERTBOT_DOMAIN'].split('.')[-2:])


class GlesysRest(object):
    username = sys.environ['GLESYS_USERNAME']
    api_key = sys.environ['GLESYS_API_KEY']
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
	validation = sys.environ['CERTBOT_VALIDATION']
	glesys.post('domain', 'addrecord', {
		'domain': domain, 'host': host, 'type': 'TXT', 'data': validation
	})

def cleanup():
	result = glesys.post('domain', 'listrecords', { 'domainname': domain })
	for record in result['records']:
		if record['host'] == host:
			glesys.post('domain', 'deleterecord', {
                		'recordid': record_id
		        })


if __name__ == "main":
	if sys.argv[1] == 'auth':
		auth()
	elif sys.argv[1] == 'cleanup':
		cleanup()
