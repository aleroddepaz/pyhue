import StringIO
import collections


class MockHTTPConnection(object):
    """
    Mock class for HTTPConnection
    """
    requests = []
    
    def __init__(self, ip_address=None):
        with open('responses') as f:
            self.responses = collections.defaultdict(list)
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