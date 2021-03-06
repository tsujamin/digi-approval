name             'app'
maintainer       'DigiACTive Pty Ltd'
maintainer_email 'digiactive.canberra@gmail.com'
license          'All rights reserved'
description      'Installs/Configures app'
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          '0.1.0'

depends 'python'
depends 'python-build'
# for development firewall hole-poking
depends 'simple_iptables'
# while we still have our own git version of packages
depends 'git'
