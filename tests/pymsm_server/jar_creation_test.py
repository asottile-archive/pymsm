
import contextlib
import flask
import mock
import pyquery
import markupsafe
import testify as T

from presentation.jar_downloader import JarDownloader
import pymsm_server.jar_creation
from pymsm_server.jar_creation import get_jar_create_form
from pymsm_server.jar_creation import get_jar_downloader_presenters
from testing.data.generators import get_fake_jar_downloader_cls

class TestGetJarDownloaderPresenters(T.TestCase):
    def test_get_jar_downloader_presenters(self):
        fake_jar_downloaders = [
            get_fake_jar_downloader_cls('C'),
            get_fake_jar_downloader_cls('A'),
            get_fake_jar_downloader_cls('B'),
        ]

        with mock.patch.object(
            pymsm_server.jar_creation,
            'get_jar_downloaders',
            autospec=True,
        ) as get_jar_downloaders_mock:
            get_jar_downloaders_mock.return_value = fake_jar_downloaders
            ret = get_jar_downloader_presenters()

            # Make sure they are sorted
            T.assert_equal(
                ret,
                sorted(
                    (JarDownloader(j) for j in fake_jar_downloaders),
                    key=lambda j: j.name,
                )
            )

class TestGetJarCreateForm(T.TestCase):
    @T.setup_teardown
    def patch_out_jar_downloader_map(self):
        with contextlib.nested(
            mock.patch.object(
                pymsm_server.jar_creation,
                'get_jar_downloader_map',
                autospec=True,
            ),
            mock.patch.object(flask, 'url_for', autospec=True),
        ) as (
            self.get_jar_downloader_map_mock,
            self.url_for_mock,
        ):
            self.get_jar_downloader_map_mock.return_value = dict(
                (cls.__name__, cls) for cls in [
                    get_fake_jar_downloader_cls('A'),
                    get_fake_jar_downloader_cls('B'),
                ]
            )
            self.url_for_mock.return_value = 'some_url'
            yield

    def test_has_hidden_input(self):
        jar_name = 'A'
        ret = get_jar_create_form(jar_name)
        # Should be blessed markup so it can go to the template
        T.assert_isinstance(ret, markupsafe.Markup)
        ret_pq = pyquery.PyQuery(ret)
        T.assert_equal(ret_pq.find('input[type=hidden]').val(), jar_name)
