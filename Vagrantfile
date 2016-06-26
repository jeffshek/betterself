# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  # Map Django's default port to 9000
  config.vm.network "forwarded_port", guest: 9000, host: 9000

  # make up a private_network_ip that likely isn't taken, 88 is lucky
  config.vm.network :private_network, ip: '172.28.128.5'
  config.vm.synced_folder ".", "/betterself", type: "nfs"

  # Sync as NFS for speed (NFS doesn't work for PCs, but vagrant should default to something else)
  # 1. to do NFS, need a private network
  # 2. also use bridge to create a private network this allows you to have a postgres instance
  config.vm.network "private_network", type: "dhcp", bridge: "en1: Wi-Fi (AirPort)"

  # don't need this at the moment
  config.ssh.insert_key = false

  # Provision scripts that install necessary requirements
  config.vm.provision "shell", path: "config/development/vagrant/provision_bootstrap.sh"

  # Copy a bash_profile config that can be customized
  config.vm.provision "file", source: "config/development/vagrant/developer_bash_profile", destination: "~/.bash_profile"

  # pandas takes a lot of memory to assemble
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end

end
