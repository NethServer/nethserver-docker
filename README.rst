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
  ``aqua`` zone are allowed to the MySQL/MariaDB port 3306.

More port rules can be opened to the system services with a esmith db command::

  db dockrules set customName aqua TCPPorts 12,23,56,89 UDPPorts 120,230,560,890 status enabled
  signal-event firewall-adjust

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
Portainer is an interface to manage all containers running on this host or eventually on remote hosts, a property must be enabled before to create the portainer container::

    config setprop portainer status enabled
    signal-event nethserver-docker-update

Access the Portainer user interface at ::

    https://<IP>:980/portainer/

The first time it is accessed, it asks to generate the administrative
credentials.

Docker repository
-----------------

The official repository of docker could be enabled to test the latest version ::

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

Aeria network
-------------

NethServer docker provides a docker network named Aeria that is bound to a bridge.
For bridge creation the server manager could be used.

To enable the Aeria network the bridgeAeria db prop has to be set to the name of the bridge ::

  config setprop docker bridgeAeria br0
  signal-event nethserver-docker-update

The NethServer DHCP module can be used to set IP addresses for the docker containers.
By default docker containers use random MAC addresses so fixed ones need to be set for the containers to make DHCP reservations work.

Here is an example for starting pihole in the Aeria network and set the MAC address ::

  docker run -d --name pihole -e TZ="Europe/Vienna" -e WEBPASSWORD="admin" -v "$(pwd)/etc-pihole/:/etc/pihole/" -v "$(pwd)/etc-dnsmasq.d/:/etc/dnsmasq.d/" --cap-add NET_ADMIN --net=aeria --mac-address=0e:6f:47:f7:26:1a --restart=unless-stopped pihole/pihole:latest

Aeria uses a docker plugin. To update the plugin ::

  signal-event nethserver-docker-plugin-update
