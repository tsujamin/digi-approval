# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.define "local" do |local|
    # Every Vagrant virtual environment requires a box to build off of.
    local.vm.box = "CentOS-6.4-x86_64-v20130731"
    
    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    local.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-x86_64-v20130731.box"
  
    # Network setup
    local.vm.network "private_network", ip: "192.168.2.15"
    
    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine.
  
    # django dev
    local.vm.network :forwarded_port, guest: 8000, host: 8000
    # openstack swift
    local.vm.network :forwarded_port, guest: 8080, host: 8080
    # nginx
    local.vm.network :forwarded_port, guest: 80,   host: 8888
    # rabbitmq - managment
    local.vm.network :forwarded_port, guest: 15672, host: 15672
  
    # NFS mount the /vagrant directory. Very helpful for lamson as it
    # allows for hard links.
    
    # We use bindfs to circumvent issues with NFS permissions. bindfs is unfortunately slow,
    # and using it with CentOS 6 requires our specially modified version of vagrant-bindfs.
    local.vm.synced_folder ".", "/vagrant", disabled: true
    local.vm.synced_folder ".", "/mnt/vagrant_nfs", type: "nfs"
    local.bindfs.bind_folder "/mnt/vagrant_nfs", "/vagrant"

    local.vm.provision "chef_solo" do |chef|
      chef.cookbooks_path = ["chef-repo/cookbooks", "chef-repo/site-cookbooks"]
      chef.data_bags_path = "chef-repo/data_bags"
      chef.roles_path = "chef-repo/roles"
      chef.environments_path = "chef-repo/environments"
      chef.environment = "development"
      # get this out of the way first, so we use it consistently
      # throughout the process
      chef.add_recipe("yum-epel")
      chef.add_role("web")
      chef.add_role("database")
      chef.add_role("app")
      chef.add_recipe("storage")
      chef.add_recipe("broker")
      chef.add_recipe("clamav")
    end
  end
  
  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  config.vm.provider :virtualbox do |vb|
    # Use VBoxManage to customize the VM.
    vb.customize ["modifyvm", :id, "--memory", "2048", "--cpus", "2"]
  end

end
