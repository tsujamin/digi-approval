web Cookbook
============

This cookbook does misc setup of the web server. Currently it just punches holes in the firewall for HTTP and SSH.

TODO: HTTPS, certs etc.

Requirements
------------

Requires iptables.

#### packages
- `iptables`: iptables.

Attributes
----------

Currently no attributes.

Usage
-----
#### web::default

Just include `web` in your node's `run_list`:

```json
{
  "name":"my_node",
  "run_list": [
    "recipe[web]"
  ]
}
```

