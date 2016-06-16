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

  # Sync as NFS for speed, but might have an issue with PCs
  # to do NFS, neet a private network
  config.vm.network "private_network", type: "dhcp"
  config.vm.synced_folder ".", "/betterself", type: "nfs"

  # don't need this at the moment
  config.ssh.insert_key = false

  # Provision scripts that install necessary requirements
  config.vm.provision "shell", path: "config/development/vagrant/provision_bootstrap.sh"

  # Copy a bash_profile config that can be customized
  config.vm.provision "file", source: "config/development/vagrant/developer_bash_profile", destination: "~/.bash_profile"

end
