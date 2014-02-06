#!/usr/bin/ruby

# we cheat big time here - rather than going through chef properly, we just
# load up an environment file and use it to render and run the relevant erb
# files from our app cookbook.

# Why such an atrocity?
#  - I am opposed to spending 2 days getting chef-solo to run inside Travis CI
#  - I am opposed to having a different system to provide local_settings and 
#    init_django to anywhere else.
# This solution means that we get the same base structure: things are defined
# in an environment file and rendered from templates, without going through
# chef. It should mean this file only needs to be adjusted when we add an erb
# template or do anything else particularly unusual.

require 'erubis'
require 'json'

settings = JSON.parse(File.read('chef-repo/environments/travis.json'))
template = File.read('chef-repo/site-cookbooks/app/templates/default/local_settings.py.erb')
template = Erubis::Eruby.new(template.gsub("@","")) # convert instance to local vars

File.open('src/digiapproval_project/digiapproval_project/local_settings.py', 'w') { |file|
    file.write(template.result(settings['default_attributes']['digiactive']))
}

template = File.read('chef-repo/site-cookbooks/app/templates/default/init_django.bash.erb')
template = Erubis::Eruby.new(template.gsub("@","")) # convert instance to local vars

File.open('/tmp/init_django.bash', 'w') { |file|
    file.write(template.result(settings['default_attributes']['digiactive']))
}

`bash /tmp/init_django.bash`
