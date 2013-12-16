# Getting started

## Submodules ##

Do this the first time you check out the repository:
```shell
git submodule init
git submodule update
```

## Chef ##

### Setup ###

```shell
# recommended but not essential: create a rvm for chef
rvm use 2.0.0@chef --create 

gem install chef 
# if using w/o rvm, do sudo gem install
```

# Regular use #

## Hacking on chef ##

```shell
rvm use 2.0.0@chef

cd chef-repo

# do knife commands, e.g.
knife cookbook site install nginx
```

If you make changes, do ```vagrant provision``` to avoid the whole destroy/up rigmarole.

If you're having trouble figuring out what's going on (yay async!), then ```vagrant ssh``` in and do:

```shell
sudo -s
chef-solo -c /tmp/vagrant-chef-1/solo.rb -j /tmp/vagrant-chef-1/dna.json 
```

You'll get *lots* more output. **Don't do this if you've just changed the Vagrantfile.**

## Database ##

Per ```/var/lib/pgsql/data/pg_hba.conf```, local connections are via ident and therefore must be with the psql user. Circumvernt this by connecting on localhost:
```shell
psql django django_user -h 127.0.0.1
```

Password is set in the django_db cookbook in the default recipe, for now.

## App ##

```shell
vagrant ssh

cd /vagrant/src/digiapproval_project/
source ../../env/bin/activate
python manage.py runserver 0.0.0.0:8000
```

The superuser's username is "super" and the password is "startthecode". (It's defined in ```chef-repo/environments/development.json```.)

## Storage ##
Hack on it with the following credentials:
```shell
swift --os-username demo --os-tenant-name demo --os-password password --os-auth-url http://127.0.0.1:5000/v2.0 stat
```

# Frequently Encountered Problems #

+ **I've lost network access in the guest**: have you moved networks? Do a ```vagrant reload``` and try again.
