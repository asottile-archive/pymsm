<%!
import flask
%>

<%inherit file="../base.mako" />

<%block name="title">Jars!</%block>

<h2>User Jars</h2>
<ul>
  % for jar_type, jars_of_type in user_jars.iteritems():
    <li>
      ${jar_type}:
      <ul>
        % for user_jar_name in jars_of_type.keys():
          <li>
            <a href="${
              flask.url_for(
                'jar.jar_home',
                jar_type=jar_type,
                user_jar_name=user_jar_name,
              )
            }">
              ${user_jar_name}
            </a>
          </li>
        % endfor
      </ul>
    </li>
  % endfor
</ul>
<h2>Create a New Jar</h2>
<ul>
  % for jar_downloader in jar_downloaders:
    <li>
      <a href="${jar_downloader.url}">
        Create new ${jar_downloader.name}
      </a>
    </li>
  % endfor
</ul>
