django_db Cookbook
==================

Creates a database and user for django.

Requirements
------------

#### packages
- `database` - django_db needs database to ... do database stuff, oddly enough.
- `postgresql` - we're using postgres

Attributes
----------

Presently none.

Usage
-----
#### django_db::default

e.g.
Just include `django_db` in your node's `run_list`:

```json
{
  "name":"my_node",
  "run_list": [
    "recipe[django_db]"
  ]
}
```

