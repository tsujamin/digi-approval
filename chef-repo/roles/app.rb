name "app"
description "Application server"

default_attributes 'python_build' => { "versions" => ["3.3.3"],
                                       "packages" => ["pip", "virtualenv"] }

run_list "recipe[python-build]",
         "app"



