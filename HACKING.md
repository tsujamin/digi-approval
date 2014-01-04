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

scl enable python27 bash

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

There are some settings in the chef development environment. Don't change these becaues localrc for devstack doesn't actually honour them at all. (And several are fixed in devstack anyway.)

## Message Broker/Queue (RabbitMQ) ##
Credentials are guest:guest.

Web interface is at http://localhost:15672/

Start workers from within ```/vagrant/src/digiapproval_project``` with ```celery -A digiapproval_project worker -l info```.

Here's code to simply exercise:
```python
from digiapproval_project.celery import debug_task
a = debug_task.delay()
print(a.status)
print(a.result)
```

## Proposed structure for task data dict
**Required**, _arbitrary key name_
{
  **view**:                                   #the template to be applied to this task
  **actor**: (approver/customer)              #the user who performs the task
  fields: {                                   #fields present in task, its contents depend on the view
    _simplename_: {                           #field
      **name**:                               #Presentable name of field
      **type**: (int/str)                     #input type of field
      **required**: (True/False)              #mandatory status of field
      value:                                  #actual value of the field
    }
  }
  data: {                                     #arbitrary static pieces of data 
    _simplename_: value
  }
  options: {                                  #options specific to the view
    _simplename_: value
  }
}

# Frequently Encountered Problems #

+ **I've lost network access in the guest**: have you moved networks? Do a ```vagrant reload``` and try again.

+ **I've lost my storage layer**: it doesn't start on boot. Do a ```vagrant provision``` to get it back.
