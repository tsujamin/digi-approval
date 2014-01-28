# Getting started

## Submodules ##

Do this the first time you check out the repository:
```shell
git submodule init
git submodule update
```

## vagrant-bindfs ##
Install our modified vagrant-bindfs plugin with CentOS 6 bindfs installation support:
```shell
wget http://digiactive.com.au/digiactive-repo/gems/vagrant-bindfs-0.2.4.digiactive2.gem
vagrant plugin install vagrant-bindfs-0.2.4.digiactive2.gem
```

## vagrant-aws ##

```shell
vagrant plugin install vagrant-aws
```

Grab the SSH key (`digiawspem.pem`) and put it in `~/.ssh`, with appropriate permissions (600).

## Chef Development Only ##

### Setup ###

```shell
# recommended but not essential: create a rvm for chef
rvm use 2.0.0@chef --create 

gem install chef 
# if using w/o rvm, do sudo gem install
```

# Regular use #

## Basic Usage ##

 * Local: ```vagrant up local```
 * AWS omnibus: ```vagrant up aws --provider aws```. Be warned that output from Chef comes in very, very delayed chunks, rather than being live. You'll also need to reboot the machine for it to pick up the firewall rules. Avoid vagrant reload because that causes things to change IP address. Of course, by rebooting, you'll lose the devstack.
 * AWS storage only: try not to touch this - it's running nicely and changing it requires poking around in rofltron's dns.
 * AWS mini: `vagrant up aws-mini --provider aws`. Same caveats about firewalls apply, except rebooting doesn't affect storage any more.

### Easy new way ###

```shell
vagrant ssh machine-of-your-choice
/vagrant/src/dev/init.sh
```

You're now in tmux - use Ctrl-b, Ctrl-[n,p] to move to the [next, previous] terminal.
Celery and Django are automatically spun up for you.

### Hard old way ###

```shell
vagrant ssh [aws|local]

scl enable python27 bash

cd /vagrant/src/digiapproval_project/
source ../../env/bin/activate
python manage.py runserver 0.0.0.0:8000
```

The superuser's username is "super" and the password is "startthecode". (It's defined in ```chef-repo/environments/development.json```.)

## Hacking on AWS ##

Files are put on AWS with Rsync. However, things are only rsynced (rsunk?) on `up`, `provision`, and `reload`, which is kind of infrequent.

If you want to manually do it, you're looking at something like:

```shell
/usr/bin/rsync --verbose --archive -z --exclude .vagrant/ --exclude Vagrantfile --exclude env --exclude chef-repo --exclude design --exclude casestudy --exclude pitch --exclude scope --exclude vagrant --exclude cookbooks --exclude .git --exclude "*.pyc" --exclude __pycache__ --exclude node_modules -e "ssh -p 22 -o StrictHostKeyChecking=no -i '/HOMEPATH/YOU/.ssh/digiawspem.pem'" /path/to/digi-approval/ ec2-user@THE_IP_ADDRESS:/vagrant
```

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

## Mail (lamson) ##

### AWS ###
If you're on AWS, you automatically get the ability to send real email. You also get an SMTP server running on 25. If you want it to recieve email, you need to set Route 53 to point mail.digiactive.com.au at your instance. You can then send email with e.g. gmail.

### Local ###
If you're on a local machine, you can recieve emails on port 25 still, and they'll be processed by lamson as per normal. You can send an email like so:
```shell
lamson send -body YOURBODYHERE -sender EMAILADDRESS -to EMAILADDRESS@digiactive.com.au -subject SUBJECT -port 25
```

In order to see the emails that Django sends, you need to:
```shell
cd /vagrant/src/digiactive_project/digimail
lamson log
tail -f logs/logger.log
```

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
  **form**:                                   #the form template to be applied to this task
  **actor**: (approver/customer)              #the user who performs the task
  fields: {                                   #fields present in task, its contents depend on the view
    _simplename_: {                           #field
      **label**:                               #Presentable name of field
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

## Demo DB Data
If you would like to fill the database with some test user accounts/orginisations call:
```shell
vagrant ssh

scl enable python27 bash

cd /vagrant/src/digiapproval_project/
source ../../env/bin/activate
python manage.py init\_demo\_db
```
**Waring** The only model instance that survives this command is the super account

# Frequently Encountered Problems #

+ **I've lost network access in the guest**: have you moved networks? Do a ```vagrant reload``` and try again.

+ **I've lost my storage layer**: it doesn't start on boot. Do a ```vagrant provision``` to get it back.
