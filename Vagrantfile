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
      # web role is useless atm
      #chef.add_role("web")
      chef.add_role("database")
      chef.add_role("app")
      chef.add_recipe("storage")
      chef.add_recipe("broker")
      chef.add_recipe("clamav")
    end
  end
  
  config.vm.define "aws" do |aws|
    aws.vm.box = "dummy"
    aws.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

    # make this a little less painful
    aws.vm.synced_folder ".", "/vagrant", :rsync_excludes=>["env", # no point in syncing that, it'll be built at that end
                                                            "chef-repo", # this is synced elsewhere
                                                            "design", "casestudy", "pitch", "scope", # unnecessary & big
                                                            "vagrant", "cookbooks", # vestigal
                                                            ".git", "*.pyc", "__pycache__", "node_modules" # sigh
                                                           ]

    
    aws.vm.provision "chef_solo" do |chef|
      chef.cookbooks_path = ["chef-repo/cookbooks", "chef-repo/site-cookbooks"]
      chef.data_bags_path = "chef-repo/data_bags"
      chef.roles_path = "chef-repo/roles"
      chef.environments_path = "chef-repo/environments"
      chef.environment = "awsdev"
      chef.add_recipe("simple_iptables")
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

  config.vm.define "aws-mini" do |aws|
    aws.vm.box = "dummy"
    aws.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

    # make this a little less painful
    aws.vm.synced_folder ".", "/vagrant", :rsync_excludes=>["env", # no point in syncing that, it'll be built at that end
                                                            "chef-repo", # this is synced elsewhere
                                                            "design", "casestudy", "pitch", "scope", # unnecessary & big
                                                            "vagrant", "cookbooks", # vestigal
                                                            ".git", "*.pyc", "__pycache__", "node_modules" # sigh
                                                           ]

    
    aws.vm.provision "chef_solo" do |chef|
      chef.cookbooks_path = ["chef-repo/cookbooks", "chef-repo/site-cookbooks"]
      chef.data_bags_path = "chef-repo/data_bags"
      chef.roles_path = "chef-repo/roles"
      chef.environments_path = "chef-repo/environments"
      chef.environment = "awsmini"
      chef.add_recipe("simple_iptables")
      # get this out of the way first, so we use it consistently
      # throughout the process
      chef.add_recipe("yum-epel")
      # web role is useless atm
      #chef.add_role("web")
      chef.add_role("database")
      chef.add_role("app")
      chef.add_recipe("broker")
      chef.add_recipe("clamav")
    end
  end


  config.vm.define "aws-storage" do |aws|
    aws.vm.box = "dummy"
    aws.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

    # make this a little less painful
    aws.vm.synced_folder ".", "/vagrant", :rsync_excludes=>["env", # no point in syncing that, it'll be built at that end
                                                            "chef-repo", # this is synced elsewhere
                                                            "design", "casestudy", "pitch", "scope", # unnecessary & big
                                                            "vagrant", "cookbooks", # vestigal
                                                            ".git", "*.pyc", "__pycache__", "node_modules" # sigh
                                                           ]

    
    aws.vm.provision "chef_solo" do |chef|
      chef.cookbooks_path = ["chef-repo/cookbooks", "chef-repo/site-cookbooks"]
      chef.data_bags_path = "chef-repo/data_bags"
      chef.roles_path = "chef-repo/roles"
      chef.environments_path = "chef-repo/environments"
      chef.environment = "awsdev"
      chef.add_recipe("simple_iptables")
      # get this out of the way first, so we use it consistently
      # throughout the process
      chef.add_recipe("yum-epel")
      # web role is useless atm
      #chef.add_role("web")
      chef.add_recipe("storage")
    end
  end

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  config.vm.provider :virtualbox do |vb|
    # Use VBoxManage to customize the VM.
    vb.customize ["modifyvm", :id, "--memory", "2048", "--cpus", "2"]
  end

  config.vm.provider :aws do |aws, override|
    aws.access_key_id = "AKIAJSDNWPSHVYBOMFGA"
    aws.secret_access_key = "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"
    aws.keypair_name = "digiaws.pem"

    aws.ami = "ami-a25415cb"
    aws.instance_type = "m1.small"

    aws.security_groups = ["digiapproval-basic"]
    
    # allow sudo without a tty; required for provisioning.
    # also install chef.
    aws.user_data = "#!/bin/bash
echo 'Defaults:ec2-user !requiretty' > /etc/sudoers.d/999-vagrant-cloud-init-requiretty && chmod 440 /etc/sudoers.d/999-vagrant-cloud-init-requiretty
curl -L https://www.opscode.com/chef/install.sh | bash"

    override.ssh.username = "ec2-user"
    override.ssh.private_key_path = "~/.ssh/digiawspem.pem"
  end
end
