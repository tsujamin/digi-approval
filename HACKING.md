# Chef

## Setup
```shell
# recommended but not essential: create a rvm for chef
rvm use 2.0.0@chef --create 

gem install chef 
# if using w/o rvm, do sudo gem install
```

## Regular use
```shell
rvm use 2.0.0@chef

cd chef-repo

# do knife commands, e.g.
knife cookbook site install nginx
```

If you make changes, do ```vagrant provision``` to avoid the whole destroy/up rigmarole.

# Database
Per ```/var/lib/pgsql/data/pg_hba.conf```, local connections are via ident and therefore must be with the psql user. Circumvernt this by connecting on localhost:
```shell
psql django django_user -h 127.0.0.1```

Password is set in the django_db cookbook in the default recipe, for now.
