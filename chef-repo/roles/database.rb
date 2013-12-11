name "database"
description "Pure Database Server"

default_attributes 'postgresql' => { 'config_pgtune' => {'dbtype' => "web"},
  'password' => {'postgres' => "Shut up and take my paperwork!"} }

run_list "recipe[postgresql::server]",
    "recipe[postgresql::config_initdb]",
    "recipe[postgresql::config_pgtune]",
    "recipe[django_db]",
    # for debugging
    "recipe[postgresql::client]"



