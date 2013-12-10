```shell
## Setup
# create a rvm for chef
rvm use 2.0.0@chef --create 

gem install chef # w/o rvm, sudo gem install


## regular use
rvm use 2.0.0@chef

cd chef-repo

# do knife commands, e.g.
knife cookbook site install nginx
```

If you make changes, do ```vagrant provision``` to avoid the whole destroy/up rigmarole.