<%!
import flask
%>

<%inherit file="base.mako" />

<%block name="title">Index</%block>

% if is_internal:
  <a href="${flask.url_for('jar_creation.jar_list')}">Jar List</a>
% endif
Hello World
