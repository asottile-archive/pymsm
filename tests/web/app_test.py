
import flask
import testify as T

from testing.assertions.response import assert_no_response_errors
from testing.base_classes.pymsm_server_test_case import PymsmServerTestCase

class TestIndex(PymsmServerTestCase):

    def _get_jar_list_selector(self):
        return '[href="{0}"]'.format(flask.url_for('jar_creation.jar_list'))

    def test_index_external_does_not_expose_jar_list(self):
        response = self.client.get(flask.url_for('index'))
        assert_no_response_errors(response)
        T.assert_length(response.pq.find(self._get_jar_list_selector()), 0)

    def test_index_internal_exposes_jar_list(self):
        with self.client.patch_ip('127.0.0.1'):
            response = self.client.get(flask.url_for('index'))
            assert_no_response_errors(response)
            T.assert_length(response.pq.find(self._get_jar_list_selector()), 1)
