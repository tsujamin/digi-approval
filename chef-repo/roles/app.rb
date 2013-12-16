name "app"
description "Application server"

default_attributes 'python_build' => { "versions" => ["3.3.3"],
                                       "packages" => [] }


run_list         "app"



