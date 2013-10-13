<%inherit file="../base.mako" />

<%block name="title">${user_jar.jar_type} | ${user_jar.name}</%block>

<%block name="scripts">
  ${parent.scripts()}
  <script>
    $(function () {
        'use strict';

        var updateLink = $('[data-update-url]'),
            updateUrl = updateLink.data('update-url'),
            downloadList = $('[data-download-url]'),
            downloadUrl = downloadList.data('download-url');

        function updateCallback(d) {
            console.log('update');
            console.log(d)
        }

        function update() {
            $.post(updateUrl, updateCallback);
        }

        function downloadCallback(d) {
            console.log('download');
            console.log(d);
        }

        function download() {
            var version = $(this).data('version');
            $.post(downloadUrl, {version: version}, downloadCallback);
        }

        updateLink.click(update);
        downloadList.delegate('[data-version]', 'click', download);
    });
  </script>
</%block>

<h2>${user_jar.jar_type} | ${user_jar.name}</h2>

<h4>Jar Directory: ${user_jar.jar_directory}</h4>

<h4>
  Latest Downloaded Version:
  ## XXX: this is totally wrong, no idea why this passes in jinja world
  % if isinstance(user_jar.latest_downloaded_version, basestring):
    ${user_jar.latest_downloaded_version}
  % else:
    ${user_jar.latest_downloaded_version.short_version}
  % endif
</h4>

<h3>Downloaded Jar Versions</h3>
<ul>
  % for jar_object in user_jar.downloaded_versions:
    <li>${jar_object.short_version}</li>
  % else:
    <li>No Jars Downloaded!</li>
  % endfor
</ul>

<h3>Available Jar Versions</h3>
<ul data-download-url="${user_jar.download_url}">
  % for jar_version in user_jar.available_versions:
    <li>
      ${jar_version}
      % if not user_jar.has_version(jar_version):
        <a href="javascript:;" data-version="${jar_version}">
          Download
        </a>
      % endif
    </li>
  % else:
    <li>No Available Versions</li>
  % endfor
</ul>

<a href="javascript:;" data-update-url="${user_jar.update_url}">
  Update
</a>

