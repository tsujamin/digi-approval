name "database"
description "Pure Database Server"

default_attributes 'postgresql' => { 'config_pgtune' => {'dbtype' => "web"},
                                     'version' => '9.3',
                                     'enable_pgdg_yum' => true
                                   }
# Password is set in environment (e.g. development.json)

run_list "recipe[postgresql::yum_pgdg_postgresql]",
         "recipe[postgresql::server]",
         "recipe[postgresql::config_initdb]",
         "recipe[postgresql::config_pgtune]",
         "recipe[django_db]",
         # for debugging
         "recipe[postgresql::client]"



