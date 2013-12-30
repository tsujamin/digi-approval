# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "CentOS-6.4-x86_64-v20130731"
  
  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-x86_64-v20130731.box"

  # Network setup
  config.vm.network "private_network", ip: "192.168.2.15"
  
  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine.

  # django dev
  config.vm.network :forwarded_port, guest: 8000, host: 8000
  # openstack swift
  config.vm.network :forwarded_port, guest: 8080, host: 8080
  # nginx
  config.vm.network :forwarded_port, guest: 80,   host: 8888
  # rabbitmq - managment
  config.vm.network :forwarded_port, guest: 15672, host: 15672

  # NFS mount the /vagrant directory. Very helpful for lamson as it
  # allows for hard links.
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  config.vm.provider :virtualbox do |vb|
    # Use VBoxManage to customize the VM.
    vb.customize ["modifyvm", :id, "--memory", "2048", "--cpus", "2"]
  end

  # Provision the environment to include the required packages
  # config.vm.provision :shell, :path => "vagrant/bootstrap.sh"
  config.vm.provision "chef_solo" do |chef|
    chef.cookbooks_path = ["chef-repo/cookbooks", "chef-repo/site-cookbooks"]
    chef.data_bags_path = "chef-repo/data_bags"
    chef.roles_path = "chef-repo/roles"
    chef.environments_path = "chef-repo/environments"
    chef.environment = "development"
    # get this out of the way first, so we use it consistently
    # throughout the process
    chef.add_recipe("yum-epel")
    # web role is useless atm
    #chef.add_role("web")
    chef.add_role("database")
    chef.add_role("app")
    chef.add_recipe("storage")
    chef.add_recipe("broker")
    chef.add_recipe("clamav")
  end
end
