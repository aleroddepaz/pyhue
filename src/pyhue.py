#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
try:
    from httplib import HTTPConnection
except ImportError:
    from http.client import HTTPConnection


kelvin2mired = lambda k: 10**6 / k
huedegree2hue = lambda d: d* 182


def cmyk2hsb(c, m, y, k):
    pass


def rgb2xy(r, g, b):
    X = 0.412453 * r + 0.357580 * g + 0.180423 * b
    Y = 0.212671 * r + 0.715160 * g + 0.072169 * b
    Z = 0.019334 * r + 0.119193 * g + 0.950227 * b
    x = X / (X+Y+Z)
    y = Y / (X+Y+Z)
    return x, y


class HueException(Exception):
    pass


class Bridge(object):
    def __init__(self, ip_address, username):
        self.ip_address = ip_address
        self.username = username

    def _request(self, method, route, data={}):
        content = json.dumps(data).lower()
        list_route = map(str, ['/api', self.username] + route)
        str_route = '/'.join(list_route)
        try:
            conn = HTTPConnection(self.ip_address)
            conn.request(method, str_route, content)
            response = conn.getresponse()
            return json.loads(response.read().decode())
        except:
            raise HueException("Not able to connect to the bridge")

    def __get_api_objects(self, cls):
        result = self._request('GET', [cls.ROUTE])
        objects = [cls(self, i) for i in result.keys()]
        return sorted(objects, key=lambda x: x.id)

    @property
    def lights(self):
        return self.__get_api_objects(Light)

    @property
    def groups(self):
        return [Group(self, 0)] + self.__get_api_objects(Group)

    @property
    def schedules(self):
        return self.__get_api_objects(Schedule)
    
    def get_light(self, light_id):
        return Light(self, light_id)

    def add_schedule(self, schedule_attrs):
        return self._request('POST', ['schedules'], schedule_attrs)


class AssignableSetattr(type):
    def __new__(mcls, name, bases, attrs):  # @NoSelf
        def __setattr__(self, attr, value):
            object.__setattr__(self, attr, value)

        init_attrs = dict(attrs)
        init_attrs['__setattr__'] = __setattr__
        base = super(AssignableSetattr, mcls)
        init_cls = base.__new__(mcls, name, bases, init_attrs)
        real_cls = base.__new__(mcls, name, (init_cls,), attrs)
        init_cls.__real_cls = real_cls
        return init_cls

    def __call__(cls, *args, **kwargs):  # @NoSelf
        self = super(AssignableSetattr, cls).__call__(*args, **kwargs)
        real_cls = cls.__real_cls
        self.__class__ = real_cls
        return self


class ApiObject(object):
    __metaclass__ = AssignableSetattr

    def __init__(self, bridge, _id):
        result = bridge._request('GET', [self.ROUTE, _id])
        if any('error' in x for x in result):
            raise HueException(result['error']['description'])
        self.bridge = bridge
        self.id = _id
        for attr, value in result.items():
            setattr(self, attr, value)

    def set(self, attr, value):
        object.__setattr__(self, attr, value)
        api_route = [self.ROUTE, self.id]
        return self.bridge._request('PUT', api_route, {attr: value})


class Light(ApiObject):
    ROUTE = 'lights'

    def update(self, **kw):
        self.state.update(kw)
        api_route = [self.ROUTE, self.id, 'state']
        return self.bridge._request('PUT', api_route, kw)

    def __setattr__(self, attr, value):
        if attr in self.state:
            result = self.update(**{attr: value})
        else:
            result = self.set(attr, value)
        if any('error' in confirmation for confirmation in result):
            raise HueException("Invalid attribute")

    def __getattr__(self, attr):
        if attr in self.state:
            return self.state[attr]
        else:
            return object.__getattr__(self, attr)


class Group(ApiObject):
    ROUTE = 'groups'

    def update(self, **kw):
        self.action.update(kw)
        api_route = [self.ROUTE, self.id, 'action']
        return self.bridge._request('PUT', api_route, kw)

    def __setattr__(self, attr, value):
        if attr in self.action:
            result = self.update(**{attr: value})
        else:
            result = self.set(attr, value)
        if any('error' in confirmation for confirmation in result):
            raise HueException("Invalid attribute")

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
            raise HueException("Invalid attribute")

    def __del__(self):
        self.bridge._request('DELETE', [self.ROUTE, self.id])
