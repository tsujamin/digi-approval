#! /bin/bash
#Based on the SAIO documentation by openstack.org

#Install dependancies
apt-get -y install swift swift-object swift-account swift-container swift-proxy curl gcc memcached rsync sqlite3 xfsprogs git-core libffi-dev python-setuptools python-coverage python-dev python-nose python-simplejson python-xattr python-eventlet python-greenlet python-pastedeploy python-netifaces python-pip python-dnspython python-mock 

#Configure storage
truncate -s 1GB /srv/swift-disk
mkfs.xfs /srv/swift-disk
echo "/srv/swift-disk /mnt/sdb1 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0" >> /etc/fstab
mkdir /mnt/sdb1
mount /mnt/sdb1
mkdir /mnt/sdb1/1 /mnt/sdb1/2 /mnt/sdb1/3 /mnt/sdb1/4
chown vagrant:vagrant /mnt/sdb1/*
for x in {1..4}; do ln -s /mnt/sdb1/$x /srv/$x; done
mkdir -p /etc/swift/object-server /etc/swift/container-server /etc/swift/account-server /srv/1/node/sdb1 /srv/2/node/sdb2 /srv/3/node/sdb3 /srv/4/node/sdb4 /var/run/swift
chown -R vagrant:vagrant /etc/swift /srv/[1-4]/ /var/run/swift 

#Configure rsync
cp -f /vagrant/vagrant/rsyncd.conf /etc/
echo "RSYNC_ENABLE=true" >> /etc/default/rsync

#Move swift configuration
cp -rf /vagrant/vagrant/swift-config/* /etc/swift/

#Move swift scripts
chmod a+x /vagrant/vagrant/swift-scripts/*
cp -f /vagrant/vagrant/swift-scripts/* /usr/bin/

#Add admin config to profile
echo "export ST_AUTH=http://localhost:8080/auth/v1.0
export ST_USER=admin:admin
export ST_KEY=admin" >> /etc/profile
. /etc/profile

#Update profile
echo "export SWIFT_TEST_CONFIG_FILE=/etc/swift/test.conf" >> /etc/profile
. /etc/profile

#Configure swift
remakerings
startmain
startrest


