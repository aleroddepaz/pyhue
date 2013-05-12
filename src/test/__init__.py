import re
import unittest
import pyhue


from mockhttpconnection import MockHTTPConnection
pyhue.HTTPConnection = MockHTTPConnection


class TestPyhue(unittest.TestCase):
    def setUp(self):
        MockHTTPConnection.requests = []
        self.bridge = pyhue.Bridge('0.0.0.0', 'username')

    def tearDown(self):
        self.bridge = None

    def assertMatches(self, string, pattern):
        return re.match(pattern, string) is not None


class TestLight(TestPyhue):
    def test_get_lights(self):
        _ = self.bridge.lights
        self.assertMatches(MockHTTPConnection.requests[0],
                           'GET /api/(.+?)/lights')
        self.assertMatches(MockHTTPConnection.requests[1],
                           'GET /api/(.+?)/lights/1')

    def test_set_light_state(self):
        lights = self.bridge.lights
        lights[0].on = True
        self.assertMatches(MockHTTPConnection.requests[2],
                           'PUT /api/(.+?)/lights/1/state')

    def test_check_light_state(self):
        lights = self.bridge.lights
        lights[0].hue = 0
        self.assertEqual(lights[0].hue, 0)

    def test_set_light_attrs(self):
        lights = self.bridge.lights
        lights[0].name = "Another Mock Lamp"
        self.assertMatches(MockHTTPConnection.requests[2],
                           'PUT /api/(.+?)/lights/1')


class TestGroups(TestPyhue):
    def test_get_groups(self):
        _ = self.bridge.groups
        self.assertMatches(MockHTTPConnection.requests[0],
                           'GET /api/(.+?)/groups')
        self.assertMatches(MockHTTPConnection.requests[1],
                           'GET /api/(.+?)/groups/1')

    def test_set_group_state(self):
        groups = self.bridge.groups
        groups[0].on = True
        self.assertMatches(MockHTTPConnection.requests[2],
                           'PUT /api/(.+?)/groups/1/action')

    def test_check_group_state(self):
        groups = self.bridge.groups
        groups[0].hue = 0
        self.assertEqual(groups[0].hue, 0)

    def test_set_group_attrs(self):
        groups = self.bridge.groups
        groups[0].name = "Another Mock Group"
        self.assertMatches(MockHTTPConnection.requests[2],
                           'PUT /api/(.+?)/groups/1')


class TestSchedules(TestPyhue):
    def test_get_schedules(self):
        _ = self.bridge.schedules
        self.assertMatches(MockHTTPConnection.requests[0],
                           'GET /api/(.+?)/schedules')
        self.assertMatches(MockHTTPConnection.requests[1],
                           'GET /api/(.+?)/schedules/1')

    def test_add_schedule(self):
        schedule_attrs = {
            "name": "Another Schedule Name",
            "description": "",
            "command": {
                "address": "/api/username/groups/1/action",
                "method": "PUT",
                "body": {"on": True}
            },
            "time": "2006-10-14T22:30:00"
        }
        self.bridge.add_schedule(schedule_attrs)
        self.assertMatches(MockHTTPConnection.requests[0],
                           'POST /api/(.+?)/schedules')

    def test_set_schedule_attrs(self):
        schedules = self.bridge.schedules
        schedules[0].name = "Another Schedule Name"
        self.assertMatches(MockHTTPConnection.requests[2],
                           'PUT /api/(.+?)/schedules/1')

    def test_delete_schedule(self):
        schedules = self.bridge.schedules
        del schedules[0]
        self.assertMatches(MockHTTPConnection.requests[2],
                           'DELETE /api/(.+?)/schedules/1')
