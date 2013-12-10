name "database"
description "Pure Database Server"

#Password: Shut up and take my paperwork!
default_attributes 'postgresql' => { 'config_pgtune' => {'dbtype' => "web"},
  'password' => {'postgres' => "md58f3d88eb36078b7d69e85a352211fdb5"} }

run_list "recipe[postgresql::server]",
    "recipe[postgresql::config_initdb]",
    "recipe[postgresql::config_pgtune]"



