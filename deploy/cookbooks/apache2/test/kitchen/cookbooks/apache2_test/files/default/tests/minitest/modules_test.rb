require File.expand_path('../support/helpers', __FILE__)

# Test all the modules that are not specifically tested through a
# Kitchenfile configuration
#
# Does not test the modules in the default_modules attribute (those
# are tested in default_test)
%w{
  apreq2
  auth_cas
  auth_digest
  authnz_ldap
  cgi
  dav_fs
  deflate
  expires
  fastcgi
  fcgid
  headers
  include
  ldap
  proxy
  proxy_balancer
  proxy_connect
  proxy_http
  rewrite
  wsgi
  xsendfile
}.each do |expected_module|

  describe "apache2::mod_#{expected_module}" do
    include Helpers::Apache

    it "installs mod_#{expected_module}" do
      apache_enabled_modules.must_include "#{expected_module}_module"
    end

  end
end
