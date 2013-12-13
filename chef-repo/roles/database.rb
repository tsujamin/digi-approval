name "database"
description "Pure Database Server"

default_attributes 'postgresql' => { 'config_pgtune' => {'dbtype' => "web"} }
# Password is set in environment (e.g. development.json)

run_list "recipe[postgresql::server]",
    "recipe[postgresql::config_initdb]",
    "recipe[postgresql::config_pgtune]",
    "recipe[django_db]",
    # for debugging
    "recipe[postgresql::client]"



