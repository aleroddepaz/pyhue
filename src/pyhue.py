import json


try:
    from httplib import HTTPConnection
except ImportError:
    from http.client import HTTPConnection


class HueException(Exception):
    pass


class Bridge(object):
    def __init__(self, ip_address, username):
        self.ip_address = ip_address
        self.username = username

    def _request(self, method, route, data={}):
        content = json.dumps(data).lower()
        str_route = '/'.join(['/api', self.username] + route)
        conn = HTTPConnection(self.ip_address)
        conn.request(method, str_route, content)
        return json.loads(conn.getresponse().read())

    @property
    def lights(self):
        result = self._request('GET', ['lights'])
        return [Light(self, i) for i in result.keys()]

    @property
    def groups(self):
        result = self._request('GET', ['groups'])
        return [Group(self, i) for i in result.keys()]


class Light(object):
    def __init__(self, bridge, _id):
        result = bridge._request('GET', ['lights', _id])
        if any('error' in x for x in result):
            raise HueException, result['error']['description']
        
        self.bridge = bridge
        self.id = _id
        self.state = result.pop('state')
        self.attrs = result
        self._initialized = True

    def __put_state(self, state):
        self.state.update(state)
        return self.bridge._request('PUT', ['lights', self.id, 'state'], state)

    def __put_name(self, name):
        self.attrs['name'] = name
        return self.bridge._request('PUT', ['lights', self.id], {'name': name})

    def __setattr__(self, attr, value):
        if getattr(self, '_initialized', False):
            pname, pstate = self.__put_name, self.__put_state
            result = pname(value) if attr == 'name' else pstate({attr: value})
            if any('error' in confirmation for confirmation in result):
                raise HueException, "Invalid attribute"
        else:
            object.__setattr__(self, attr, value)


class Group(object):
    def __init__(self, bridge, _id):
        result = bridge._request('GET', ['groups', _id])
        if any('error' in x for x in result):
            raise HueException, result['error']['description']
        
        self.bridge = bridge
        self.id = _id
