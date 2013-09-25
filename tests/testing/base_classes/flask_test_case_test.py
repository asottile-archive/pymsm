
import flask
import testify as T

from testing.base_classes.flask_test_case import FlaskTestCase

class MyError(ValueError): pass

def fail(): raise MyError

fail_app = flask.Flask(__name__)
fail_app.route('/fail')(fail)

class TestFlaskTestCase(FlaskTestCase):

    FLASK_APPLICATION = fail_app

    def test_if_endpoint_raises_exception_we_get_that_exception(self):
        with T.assert_raises(MyError):
            self.client.get('/fail')
