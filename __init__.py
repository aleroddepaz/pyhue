import json


try:
    from httplib import HTTPConnection
except ImportError:
    from http.client import HTTPConnection


class Bridge(object):
    def __init__(self, ip_address, username):
        self.ip_address = ip_address
        self.username = username

    def _request(self, method, route, data={}):
        content = json.dumps(data).lower()
        complete_route = '/'.join([self.base_route, route])
        conn = HTTPConnection(self.ip_address)
        conn.request(method, complete_route, content)
        print "%s %s%s %s" % (method, self.ip_address, complete_route, content)
        return json.loads(conn.getresponse().read())

    @property
    def base_route(self):
        return '/api/{}'.format(self.username)

    @property
    def lights(self):
        result = self._request('GET', 'lights')
        return [Light(self, i) for i in result.keys()]


class Light(object):
    def __init__(self, bridge, id):
        object.__setattr__(self, 'bridge', bridge)
        object.__setattr__(self, 'id', id)
        route = '/'.join(['lights', self.id])
        result = self.bridge._request('GET', route)
        for key, value in result.items():
            if key == "state":
                for keystate, keyvalue in value.items():
                    object.__setattr__(self, keystate, keyvalue)
            else:
                object.__setattr__(self, key, value)
                
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        route = '/'.join(['lights', self.id, 'state'])
        self.bridge._request('PUT', route, {name:value})

