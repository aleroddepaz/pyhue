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
        lights = [Light(self, i) for i in result.keys()]
        return sorted(lights, key=lambda x: x.id)

    @property
    def groups(self):
        result = self._request('GET', ['groups'])
        return [Group(self, i) for i in result.keys()]


class AssignableSetattr(type):
    def __new__(mcls, name, bases, attrs): #@NoSelf
        def __setattr__(self, attr, value):
            object.__setattr__(self, attr, value)
            
        init_attrs = dict(attrs)
        init_attrs['__setattr__'] = __setattr__
        init_cls = super(AssignableSetattr, mcls).__new__(mcls, name, bases, init_attrs)
        real_cls = super(AssignableSetattr, mcls).__new__(mcls, name, (init_cls,), attrs)
        init_cls.__real_cls = real_cls
        return init_cls

    def __call__(cls, *args, **kwargs): #@NoSelf
        self = super(AssignableSetattr, cls).__call__(*args, **kwargs)
        real_cls = cls.__real_cls
        self.__class__ = real_cls
        return self


class ApiObject(object):
    __metaclass__ = AssignableSetattr
    
    def __init__(self, bridge, _id):
        result = bridge._request('GET', [self.ROUTE, _id])
        if any('error' in x for x in result):
            raise HueException, result['error']['description']
        self.bridge = bridge
        self.id = _id
        self.attrs = result
        self.state = self.attrs.pop(self.STATE)

    def set_attrs(self, attrs):
        self.attrs.update(attrs)
        api_route = [self.ROUTE, self.id]
        return self.bridge._request('PUT', api_route, attrs)

    def set_state(self, state):
        self.state.update(state)
        api_route = [self.ROUTE, self.id, self.STATE]
        return self.bridge._request('PUT', api_route, state)


class Light(ApiObject):
    ROUTE, STATE = 'lights', 'state'
    
    def __setattr__(self, attr, value):
        d = {attr: value}
        result = self.set_attrs(d) if attr == 'name' else self.set_state(d)
        if any('error' in confirmation for confirmation in result):
            raise HueException, "Invalid attribute"

    def __getattr__(self, attr, default=None):
        if attr in self.attrs:
            return self.attrs[attr]
        elif attr in self.state:
            return self.state[attr]
        else:
            return object.__getattr__(self, attr, default)


class Group(ApiObject):
    ROUTE, STATE = 'groups', 'action'
    
    def __setattr__(self, attr, value):
        d = {attr: value}
        result = self.set_attrs(d) if attr in self.attrs else self.set_state(d)
        if any('error' in confirmation for confirmation in result):
            raise HueException, "Invalid attribute"

    def __getattr__(self, attr, default=None):
        if attr in self.attrs:
            return self.attrs[attr]
        elif attr in self.state:
            return self.state[attr]
        else:
            return object.__getattr__(self, attr, default)
