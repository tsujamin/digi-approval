name "app"
description "Application server"

default_attributes 'python_build' => { "versions" => ["2.7.6"],
                                       "packages" => ["virtualenv"] }


run_list         "app"



