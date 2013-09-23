
import pyquery

from util.decorators import cached_property

class TestingResponse(object):
    """A TestingResponse wraps a response from a testing Client."""

    def __init__(self, response):
        self.response = response

    @cached_property
    def pq(self):
        return pyquery.PyQuery(self.response.data)
