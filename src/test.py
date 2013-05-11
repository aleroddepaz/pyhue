import pyhue
import StringIO
import unittest
from collections import defaultdict


class MockHTTPConnection(object):
    """
    Mock class for HTTPConnection
    """
    requests = []
    
    def __init__(self, ip_address=None):
        with open('responses') as f:
            self.responses = defaultdict(list)
            self.__load_responses(f)
        for key, value in self.responses.items():
            self.responses[key] = ''.join(value)

    def __load_responses(self, f):
        actual = ''
        for line in f:
            if line.startswith('#'):
                actual = line[1:].strip()
            else:
                self.responses[actual].append(line)

    def request(self, method, route, content):
        """
        Mock HTTP request. Adds the method and the route
        of the request to the list of mock requests
        """
        MockHTTPConnection.requests.append('%s %s' % (method, route))
        
    def getresponse(self):
        """
        Mock response. Returns the corresponding entry of the 
        last mock request, or the error message if it does not exist
        """
        try:
            response = self.responses[MockHTTPConnection.requests[-1]]
        except KeyError:
            response = '{"error": {"description": <description>}}'
        finally:
            return StringIO.StringIO(response)

pyhue.HTTPConnection = MockHTTPConnection


class TestLight(unittest.TestCase):
    def setUp(self):
        MockHTTPConnection.requests = []
        self.bridge = pyhue.Bridge(None, '<username>')
    
    def tearDown(self):
        self.bridge = None
        
    def test_get_lights(self):
        _ = self.bridge.lights
        self.assertEqual(MockHTTPConnection.requests[0],
                         'GET /api/<username>/lights')
        self.assertEqual(MockHTTPConnection.requests[1],
                         'GET /api/<username>/lights/1')
        
    def test_set_light_state(self):
        lights = self.bridge.lights
        lights[0].on = True
        self.assertEqual(MockHTTPConnection.requests[2],
                         'PUT /api/<username>/lights/1/state')
        
    def test_check_light_state(self):
        lights = self.bridge.lights
        lights[0].hue = 0
        self.assertEqual(lights[0].hue, 0)

    def test_set_light_attrs(self):
        lights = self.bridge.lights
        lights[0].name = "Another Mock Lamp"
        self.assertEqual(MockHTTPConnection.requests[2],
                         'PUT /api/<username>/lights/1')
        

class TestGroups(unittest.TestCase):
    def setUp(self):
        MockHTTPConnection.requests = []
        self.bridge = pyhue.Bridge(None, '<username>')
        
    def test_get_groups(self):
        _ = self.bridge.groups
        self.assertEqual(MockHTTPConnection.requests[0],
                         'GET /api/<username>/groups')
        self.assertEqual(MockHTTPConnection.requests[1],
                         'GET /api/<username>/groups/1')

    def test_set_group_state(self):
        groups = self.bridge.groups
        groups[0].on = True
        self.assertEqual(MockHTTPConnection.requests[2],
                         'PUT /api/<username>/groups/1/action')
 
    def test_check_group_state(self):
        groups = self.bridge.groups
        groups[0].hue = 0
        self.assertEqual(groups[0].hue, 0)
    
    def test_set_group_attrs(self):
        groups = self.bridge.groups
        groups[0].name = "Another Mock Group"
        self.assertEqual(MockHTTPConnection.requests[2],
                         'PUT /api/<username>/groups/1')

class TestSchedules(unittest.TestCase):
    def setUp(self):
        MockHTTPConnection.requests = []
        self.bridge = pyhue.Bridge(None, '<username>')
    
    def test_get_schedules(self):
        _ = self.bridge.schedules
        self.assertEqual(MockHTTPConnection.requests[0],
                         'GET /api/<username>/schedules')
        self.assertEqual(MockHTTPConnection.requests[1],
                         'GET /api/<username>/schedules/1')

    def test_add_schedule(self):
        schedule_attrs = {
            "name": "Wake up",
            "description": "My wake up alarm",
            "command": {
                "address": "/api/0/groups/1/action",
                "method": "PUT",
                "body": { "on": True }
            },
            "time": "2011-03-30T14:24:40"
        }
        self.bridge.add_schedule(schedule_attrs)
        self.assertEqual(MockHTTPConnection.requests[0],
                         'POST /api/<username>/schedules')
    
    def test_set_schedule_attrs(self):
        schedules = self.bridge.schedules
        schedules[0].name = "Another Schedule Name"
        self.assertEqual(MockHTTPConnection.requests[2],
                         'PUT /api/<username>/schedules/0')

    def test_delete_schedule(self):
        schedules = self.bridge.schedules
        del schedules[0]
        self.assertEqual(MockHTTPConnection.requests[2],
                         'DELETE /api/<username>/schedules/0')
