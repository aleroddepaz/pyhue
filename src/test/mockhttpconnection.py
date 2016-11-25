from StringIO import StringIO
from collections import defaultdict


class MockHTTPConnection(object):
    """Mock class for HTTPConnection"""

    def __init__(self, ip_address=None):
        self.request = None
        self.responses = defaultdict(list)
        with open('responses') as f:
            self._load_responses(f)
        for key, value in self.responses.items():
            self.responses[key] = ''.join(value)

    def _load_responses(self, lines):
        actual = ''
        for line in lines:
            if line.startswith('#'):
                actual = line[1:].strip()
            else:
                self.responses[actual].append(line)

    def request(self, method, route, content):
        """Registers a mock HTTP request"""
        self.request = '%s %s' % (method, route)

    def getresponse(self):
        """Returns a mock response corresponding to the last request"""
        try:
            response = self.responses[self.request]
        except KeyError:
            response = '{"error": {"description": "mock description"}}'
        return StringIO(response)

