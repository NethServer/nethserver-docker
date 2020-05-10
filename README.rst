=================
nethserver-docker
=================

This is a prototype that integrates Docker based applications within
NethServer. 

* It defines a new firewall zone and docker network, ``aqua``. Basically, 
  containers are attached to ``aqua`` and they can talk each other. IP
  traffic from other zones, like ``green`` and ``red`` must be configured with
  the usual ``Firewall rules`` and ``Port forwarding`` pages

* As example to test integration with system services, connections from the
  ``aqua`` zone are allowed to the MySQL/MariaDB port 3306

* It exposes portainer dashboards through the
  ``httpd-admin`` Apache instance as ``https://<IP>:980/portainer/``

The default Docker *bridged* network is disabled, as long as the *iptables*
mangling feature.


Installation
------------

Install the ``nethserver-docker`` package from ``nethforge-testing`` ::

    yum install --enablerepo=nethforge-testing nethserver-docker

Configuration
-------------

If you have a free block device (required for production environments) assign it
to Docker before starting it for the first time ::

    config setprop docker DirectLvmDevice /dev/sdb

Review the current settings with ::

    config show docker

* ``Network``, is the IP network address of the ``aqua`` zone
* ``IpAddress``, is the IP address of the Docker host in the ``Network`` above

Enable the ``docker`` service and start it for the first time ::

    config setprop docker status enabled
    signal-event nethserver-docker-update

Web user interface
------------------

Access the Portainer user interface at ::

    https://<IP>:980/portainer/

The first time it is accessed, it asks to generate the administrative
credentials.

Docker repository
-----------------

The official repository of docker could be enabled to test the lastest version ::

    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    

Open Firewall For testing purpose
---------------------------------

For testing purposes you can open the docker network by policy. In a production environment you should leave this step and set firewall rules ::

  mkdir -p /etc/e-smith/templates-custom/etc/shorewall/policy
  cp /etc/e-smith/templates/etc/shorewall/policy/35aqua /etc/e-smith/templates-custom/etc/shorewall/policy/
  cat << 'EOF' > /etc/e-smith/templates-custom/etc/shorewall/policy/35aqua
  #
  # 35aqua -- the Docker network policy
  #
  aqua net ACCEPT
  $FW aqua ACCEPT
  aqua $FW ACCEPT
  loc aqua ACCEPT
  EOF
  signal-event firewall-adjust
