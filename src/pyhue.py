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

    def __get_api_objects(self, cls):
        result = self._request('GET', [cls.ROUTE])
        objects = [cls(self, i) for i in result.keys()]
        return sorted(objects, key=lambda x: x.id)

    @property
    def lights(self):
        return self.__get_api_objects(Light)

    @property
    def groups(self):
        return self.__get_api_objects(Group)
    
    @property
    def schedules(self):
        return self.__get_api_objects(Schedule)
    
    def add_schedule(self, schedule_attrs):
        return self._request('POST', ['schedules'], schedule_attrs)


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
        for attr, value in result.items():
            setattr(self, attr, value)

    def set(self, attr, value):
        object.__setattr__(self, attr, value)
        api_route = [self.ROUTE, self.id]
        return self.bridge._request('PUT', api_route, {attr:value})


class Light(ApiObject):
    ROUTE = 'lights'

    def set_state(self, newstate):
        self.state.update(newstate)
        api_route = [self.ROUTE, self.id, 'state']
        return self.bridge._request('PUT', api_route, newstate)
        
    def __setattr__(self, attr, value):
        result = self.set_state({attr: value}) if attr in self.state else self.set(attr, value)
        if any('error' in confirmation for confirmation in result):
            raise HueException, "Invalid attribute"

    def __getattr__(self, attr):
        if attr in self.state:
            return self.state[attr]
        else:
            return object.__getattr__(self, attr)


class Group(ApiObject):
    ROUTE = 'groups'
    
    def set_action(self, newstate):
        self.action.update(newstate)
        api_route = [self.ROUTE, self.id, 'action']
        return self.bridge._request('PUT', api_route, newstate)
    
    def __setattr__(self, attr, value):
        result = self.set_action({attr: value}) if attr in self.action else self.set(attr, value)
        if any('error' in confirmation for confirmation in result):
            raise HueException, "Invalid attribute"

    def __getattr__(self, attr):
        if attr in self.action:
            return self.action[attr]
        else:
            return object.__getattribute__(self, attr)


class Schedule(ApiObject):
    ROUTE = 'schedules'

    def __setattr__(self, attr, value):
        result = self.set(attr, value)
        if any('error' in confirmation for confirmation in result):
            raise HueException, "Invalid attribute"
    
    def __del__(self):
        self.bridge._request('DELETE', [self.ROUTE, self.id])
        return object.__del__(self)
