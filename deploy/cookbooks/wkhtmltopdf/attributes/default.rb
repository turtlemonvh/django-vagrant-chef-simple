default[:wkhtmltopdf][:arch] = "amd64"
default[:wkhtmltopdf][:version] = "0.11.0_rc1"
default[:wkhtmltopdf][:static_download_url] = "http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-#{node[:wkhtmltopdf][:version]}-static-#{node[:wkhtmltopdf][:arch]}.tar.bz2"
