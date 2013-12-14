app Cookbook
============

This cookbook sets up a pure application server with Django, etc.

Requirements
------------

#### Poorly modularised requirements
Requires Python 3 to be preinstalled. It's not possible to do this through the standard python cookbook, so it's assume you've figured out how to do it elsewhere.

#### packages
- `application[_python]`

Attributes
----------
Currently none.

Usage
-----
#### app::default


e.g.
Just include `app` in your node's `run_list`:

```json
{
  "name":"my_node",
  "run_list": [
    "recipe[app]"
  ]
}
```

