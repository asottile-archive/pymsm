
import __builtin__

import contextlib
import fnmatch
import mock
import os.path
import simplejson
import testify as T
import urllib2

from jar_downloader.jar_downloader_base import Jar
import jar_downloader.vanilla_jar_downloader
from jar_downloader.vanilla_jar_downloader import DOWNLOAD_PATH
from jar_downloader.vanilla_jar_downloader import get_versions_json
from jar_downloader.vanilla_jar_downloader import InvalidVersionFileError
from jar_downloader.vanilla_jar_downloader import JAR_FILENAME
from jar_downloader.vanilla_jar_downloader import JAR_MATCH
from jar_downloader.vanilla_jar_downloader import LATEST_FILE
from jar_downloader.vanilla_jar_downloader import RELEASE
from jar_downloader.vanilla_jar_downloader import SNAPSHOT
from jar_downloader.vanilla_jar_downloader import VanillaJarDownloader
from jar_downloader.vanilla_jar_downloader import VERSION_REGEX
from jar_downloader.vanilla_jar_downloader import VERSIONS_ENDPOINT
from testing.assertions.version_json import assert_json_structure
from testing.data.generators import get_fake_versions_json
from testing.utilities.fake_file import FakeFile
from util.natural_sort import natural_sort

class TestGetVersionsJson(T.TestCase):
    """Tests the get_versions_json method."""

    def test_get_versions_json(self):
        with contextlib.nested(
            mock.patch.object(simplejson, 'loads', autospec=True),
            mock.patch.object(urllib2, 'urlopen', autospec=True),
        ) as (
            loads_mock,
            urlopen_mock,
        ):
            retval = get_versions_json()
            urlopen_mock.assert_called_once_with(VERSIONS_ENDPOINT)
            loads_mock.assert_called_once_with(
                urlopen_mock.return_value.read.return_value
            )
            T.assert_equal(retval, loads_mock.return_value)

    @T.suite('integration')
    @T.suite('external')
    def test_structure_of_external_json(self):
        """A smoke test of the json data returned from the version service."""
        json_object = get_versions_json()
        assert_json_structure(json_object)


class TestVanillaJarDownloader(T.TestCase):
    """Tests the vanilla jar downloader."""

    directory = str(object())

    @T.setup_teardown
    def patch_out_base_init_verifying_directory(self):
        """Patch out JarDownloaderBase.__init__ beacuse it asserts that the
        path we are using exists.
        """

        def fake_init(fakeself, jar_directory):
            """A fake init method to bypass os.path.exists check."""
            fakeself.jar_directory = jar_directory

        with mock.patch.object(
            jar_downloader.vanilla_jar_downloader.JarDownloaderBase,
            '__init__',
            fake_init,
        ):
            yield

    @T.setup_teardown
    def patch_out_config(self):
        """Patch out VanillaJarDownloader.config"""
        with mock.patch.object(
            VanillaJarDownloader,
            'config',
            {'jar_type': RELEASE},
        ):
            yield

    @T.setup_teardown
    def patch_out_get_versions_json(self):
        with mock.patch.object(
            jar_downloader.vanilla_jar_downloader,
            'get_versions_json',
            autospec=True,
        ) as self.get_versions_json_mock:
            yield

    def test_jar_filename_regexes(self):
        version = str(object())
        filename = JAR_FILENAME % version
        T.assert_equal(VERSION_REGEX.match(filename).groups()[0], version)
        T.assert_equal(True, fnmatch.fnmatch(filename, JAR_MATCH))

    def test_latest_filename(self):
        T.assert_equal(
            VanillaJarDownloader(self.directory)._latest_filename,
            os.path.join(self.directory, LATEST_FILE)
        )

    def test_to_jar(self):
        version = str(object())
        filename = JAR_FILENAME % version
        jar_out = VanillaJarDownloader._to_jar(filename)

        T.assert_isinstance(jar_out, Jar)
        T.assert_equal(jar_out.filename, filename)
        T.assert_equal(jar_out.short_version, version)

    def test_download_versions(self):
        with mock.patch.object(os, 'listdir', autospec=True) as listdir_mock:
            listdir_mock.return_value = [
                # Some garbage
                'foo.txt',
                'foo.jar',
                'foo',
                # Some actual files that we downloaded
                JAR_FILENAME % '1.6.2',
                JAR_FILENAME % 'derp',
                JAR_FILENAME % 'herp',
            ]
            instance = VanillaJarDownloader(self.directory)
            downloaded_versions = instance.downloaded_versions
            T.assert_equal(
                downloaded_versions,
                [
                    Jar(JAR_FILENAME % '1.6.2', '1.6.2'),
                    Jar(JAR_FILENAME % 'derp', 'derp'),
                    Jar(JAR_FILENAME % 'herp', 'herp'),
                ]
            )

    def test_downloaded_versions_sorts(self):
        with mock.patch.object(os, 'listdir', autospec=True) as listdir_mock:
            listdir_mock.return_value = [
                JAR_FILENAME % '1.6.2',
                JAR_FILENAME % '1.4.5',
                JAR_FILENAME % '1.6.4',
            ]
            instance = VanillaJarDownloader(self.directory)
            downloaded_versions = instance.downloaded_versions
            T.assert_equal(
                downloaded_versions,
                [
                    Jar(JAR_FILENAME % '1.4.5', '1.4.5'),
                    Jar(JAR_FILENAME % '1.6.2', '1.6.2'),
                    Jar(JAR_FILENAME % '1.6.4', '1.6.4'),
                ],
            )

    def test_try_to_get_latest_version_file_does_not_exist(self):
        with contextlib.nested(
            mock.patch.object(os.path, 'exists', autospec=True),
            T.assert_raises(InvalidVersionFileError),
        ) as (
            exists_mock,
            _
        ):
            exists_mock.return_value = False
            VanillaJarDownloader(self.directory)._try_to_get_latest_version()

    def test_try_to_get_latest_version_jar_does_not_exists(self):
        def fake_exists(path):
            """Returns true every other time."""
            fake_exists.return_value = not fake_exists.return_value
            return fake_exists.return_value

        # Return True the first time, note it returns the opposite of what it
        # says it does
        fake_exists.return_value = False

        with contextlib.nested(
            mock.patch.object(__builtin__, 'open', autospec=True),
            mock.patch.object(os.path, 'exists', fake_exists),
            T.assert_raises(InvalidVersionFileError),
        ) as (
            open_mock,
            _,
            _,
        ):
            open_mock.return_value = FakeFile(' foo ')
            VanillaJarDownloader(self.directory)._try_to_get_latest_version()

    def test_try_to_get_latest_version_jar_exists(self):
        with contextlib.nested(
            mock.patch.object(os.path, 'exists', autospec=True),
            mock.patch.object(__builtin__, 'open', autospec=True),
        ) as (
            exists_mock,
            open_mock,
        ):
            exists_mock.return_value = True
            open_mock.return_value = FakeFile('   foo   \n')
            instance = VanillaJarDownloader(self.directory)
            latest_version = instance._try_to_get_latest_version()
            T.assert_equal(
                latest_version,
                open_mock.return_value.contents.strip(),
            )

    def test_latest_download_version(self):
        with mock.patch.object(
            VanillaJarDownloader,
            '_try_to_get_latest_version',
            autospec=True,
        ) as _try_to_get_latest_mock:
            _try_to_get_latest_mock.return_value = JAR_FILENAME % 'herp'
            instance = VanillaJarDownloader(self.directory)
            return_value = instance.latest_downloaded_version
            T.assert_equal(return_value, Jar(JAR_FILENAME % 'herp', 'herp'))

    def test_latest_download_version_trys_to_clean_up_on_failure(self):
        with contextlib.nested(
            mock.patch.object(
                VanillaJarDownloader,
                '_try_to_get_latest_version',
                autospec=True,
            ),
            mock.patch.object(os.path, 'exists', autospec=True),
            mock.patch.object(os, 'remove', autospec=True),
        ) as (
            _try_to_get_latest_mock,
            exists_mock,
            remove_mock,
        ):
            _try_to_get_latest_mock.side_effect = InvalidVersionFileError
            exists_mock.return_value = True
            instance = VanillaJarDownloader(self.directory)
            with T.assert_raises(InvalidVersionFileError):
                instance.latest_downloaded_version

            # Make sure we attempted to delete the file
            exists_mock.assert_called_once_with(instance._latest_filename)
            remove_mock.assert_called_once_with(instance._latest_filename)

    def test_available_versions_release(self):
        self.get_versions_json_mock.return_value = get_fake_versions_json()
        instance = VanillaJarDownloader(self.directory)
        versions = instance.available_versions

        T.assert_equal(
            versions,
            natural_sort([
                version_dict['id']
                for version_dict in self.get_versions_json_mock.return_value['versions']
                if version_dict['type'] == RELEASE
            ])
        )

    def test_available_versions_snapshot(self):
        with mock.patch.dict(VanillaJarDownloader.config, {'jar_type': SNAPSHOT}):
            self.get_versions_json_mock.return_value = get_fake_versions_json()
            instance = VanillaJarDownloader(self.directory)
            versions = instance.available_versions

            T.assert_equal(
                versions,
                natural_sort([
                    version_dict['id']
                    for version_dict in self.get_versions_json_mock.return_value['versions']
                    if version_dict['type'] in  set([RELEASE, SNAPSHOT])
                ])
            )

    def test_download_specific_version_version_does_not_exist(self):
        with contextlib.nested(
            mock.patch.object(
                VanillaJarDownloader,
                'available_versions',
                ['foo'],
            ),
            T.assert_raises(AssertionError),
        ):
            instance = VanillaJarDownloader(self.directory)
            instance.download_specific_version('version_dne')

    def test_download_specific_version_performs_download(self):
        version = str(object())
        with contextlib.nested(
            mock.patch.object(urllib2, 'urlopen', autospec=True),
            mock.patch.object(__builtin__, 'open', autospec=True),
            mock.patch.object(
                VanillaJarDownloader,
                'available_versions',
                [version,],
            ),
        ) as (
            urlopen_mock,
            open_mock,
            _,
        ):
            open_mock.return_value = FakeFile()
            instance = VanillaJarDownloader(self.directory)
            instance.download_specific_version(version)
            urlopen_mock.assert_called_once_with(
                DOWNLOAD_PATH.format(version=version)
            )
            open_mock.assert_called_once_with(
                os.path.join(self.directory, JAR_FILENAME % version),
                'wb',
            )
            open_mock.return_value.write.assert_called_once_with(
                urlopen_mock.return_value.read.return_value
            )

    def test_get_latest_version(self):
        release_version = '1.6.2'
        snapshot_version = '19w32a'
        self.get_versions_json_mock.return_value = get_fake_versions_json(
            release_version=release_version,
            snapshot_version=snapshot_version,
        )

        instance = VanillaJarDownloader(self.directory)

        with mock.patch.dict(
            VanillaJarDownloader.config, {'jar_type': RELEASE}
        ):
            T.assert_is(instance._get_latest_version(), release_version)

        with mock.patch.dict(
            VanillaJarDownloader.config, {'jar_type': SNAPSHOT}
        ):
            T.assert_is(instance._get_latest_version(), snapshot_version)

    def test_update_with_no_new_jar(self):
        version = str(object())
        with mock.patch.object(
            VanillaJarDownloader,
            'latest_downloaded_version',
            version,
        ):
            self.get_versions_json_mock.return_value = get_fake_versions_json(
                release_version=version,
            )
            instance = VanillaJarDownloader(self.directory)
            return_value = instance.update()
            T.assert_is(return_value, None)

    def test_update_with_new_jar(self):
        version = str(object())
        with contextlib.nested(
            mock.patch.object(
                VanillaJarDownloader,
                'download_specific_version',
                autospec=True,
            ),
            mock.patch.object(__builtin__, 'open', autospec=True),
            mock.patch.object(
                VanillaJarDownloader,
                'latest_downloaded_version',
                None,
            ),
        ) as (
            download_specific_version_mock,
            open_mock,
            _,
        ):
            self.get_versions_json_mock.return_value = get_fake_versions_json(
                release_version=version,
            )
            open_mock.return_value = FakeFile()

            instance = VanillaJarDownloader(self.directory)
            retval = instance.update()

            self.get_versions_json_mock.assert_called_once_with()
            download_specific_version_mock.assert_called_once_with(
                instance, version,
            )
            open_mock.assert_called_once_with(instance._latest_filename, 'w')
            open_mock.return_value.write.assert_called_once_with(
                JAR_FILENAME % version
            )
            T.assert_equal(retval, Jar(JAR_FILENAME % version, version))

    def test_update_with_corrupted_version_file(self):
        version = str(object())
        with contextlib.nested(
            mock.patch.object(
                VanillaJarDownloader,
                'download_specific_version',
                autospec=True,
            ),
            mock.patch.object(__builtin__, 'open', autospec=True),
            mock.patch.object(
                VanillaJarDownloader,
                'latest_downloaded_version',
                mock.PropertyMock(side_effect=InvalidVersionFileError),
            ),
        ) as (
            download_specific_version_mock,
            open_mock,
            _,
        ):
            self.get_versions_json_mock.return_value = get_fake_versions_json(
                release_version=version,
            )
            open_mock.return_value = FakeFile()

            instance = VanillaJarDownloader(self.directory)
            retval = instance.update()

            # Only really care that it updates when its version file is borked
            T.assert_equal(retval, Jar(JAR_FILENAME % version, version))
