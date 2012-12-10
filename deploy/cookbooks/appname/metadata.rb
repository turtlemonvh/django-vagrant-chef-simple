name              "webapp"
maintainer        "GTRI"
maintainer_email  "timothy.vanheest@gtri.gatech.edu"
license           "Apache 2.0"
description       "Installs needed recipies and executes commands to install python packages using pip."
version           "0.0.1"

depends           "apt"

recipe "webapp", "Installs several python packages via pip"

%w{ debian ubuntu centos redhat fedora freebsd smartos }.each do |os|
  supports os
end
