# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  # Map Django's default port to 9000
  config.vm.network "forwarded_port", guest: 8001, host: 8001
  config.vm.network "forwarded_port", guest: 5432, host: 5432

  config.vm.network :private_network, ip: '172.28.128.5'
  config.vm.synced_folder ".", "/betterself", type: "nfs"

  # Sync as NFS for speed (NFS doesn't work for PCs, but vagrant should default to something else)
  # 1. to do NFS, need a private network
  # 2. also use bridge to create a private network this allows you to have a postgres instance
  config.vm.network "private_network", type: "dhcp", bridge: "en1: Wi-Fi (AirPort)"

  # don't need this since this is not used to provision boxes
  config.ssh.insert_key = false

  config.ssh.forward_agent = true

  # pandas takes a lot of memory to assemble
  config.vm.provider "virtualbox" do |v|
    # the fact that you can use this much memory in pandas kinda scares me
    v.memory = 4096
    v.cpus = 2
  end

  # Copy a bash_profile config that can be customized
  config.vm.provision "file", source: "config/development/vagrant/developer_bash_profile", destination: "~/.bash_profile"

  # Provision scripts that install necessary requirements
  config.vm.provision "shell", path: "config/development/vagrant/provision_bootstrap.sh"

end
