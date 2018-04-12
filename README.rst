=================
nethserver-docker
=================

This is a configuration prototype to integrate Docker based applications within
NethServer. 

* It defines a new firewall zone and docker network, ``aqua``. Containers are
  attached to ``aqua``. They can talk each other and with the host machine. IP
  traffic from other zones, like ``green`` and ``red`` must be configured with
  the usual ``Firewall rules`` and ``Port forwarding`` pages

* It configures a traefik HTTP reverse-proxy instance to override the default
  Apache/httpd daemon on ports 80 and 443. Apache is still reachable through
  traefik as default backend
  
* It exposes portainer and traefik dashboards through the
  ``httpd-admin`` Apache instance

The default Docker *bridged* network is disabled, as long as the *iptables*
mangling feature.


Installation
------------

Attach a new, blank disk to your system. It is required for Docker storage.

Copy the ``root/`` dir contents from this repository to the target system.

Edit ``/etc/docker/docker.conf``, set your block device name ::
    
    "dm.directlvm_device=/dev/sdb"

Enable and start the docker daemon ::
    
    systemctl enable --now docker

Create the custom bridge network ::
    
    docker network create \
        --subnet=172.28.0.0/16 \
        --ip-range=172.28.5.0/24 \
        --gateway=172.28.5.254 \
        --opt com.docker.network.bridge.name=aqua0 \
        aqua

Configure the firewall zone ``aqua`` and related rules ::
    
    # db networks show aqua
    aqua=zone
        Description=Docker network
        Interface=aqua0
        Network=172.28.0.0/16
    
    # db fwrules show
        1=rule
            Action=accept
            Dst=any
            Log=none
            Position=64
            Service=any
            Src=zone;aqua
            status=enabled
        2=rule
            Action=accept
            Dst=zone;aqua
            Log=none
            Position=128
            Service=any
            Src=role;green
            status=enabled
        3=rule
            Action=accept
            Dst=zone;aqua
            Log=none
            Position=192
            Service=any
            Src=fw
            status=enabled
    
    # db hosts show
    portainer=host
        Description=Docker container
        IpAddress=172.28.7.0
    traefik=host
        Description=Docker container
        IpAddress=172.28.7.1
    
    # db portforward show
    1=pf
        Allow=
        Description=
        Dst=80
        DstHost=host;traefik
        OriDst=
        Proto=tcp
        Src=80
        status=enabled
    2=pf
        Allow=
        Description=
        Dst=443
        DstHost=host;traefik
        OriDst=
        Proto=tcp
        Src=443
        status=enabled
    
    # signal-event firewall-adjust

Run containers attached to ``aqua``. For instance, here we run ``portainer``
with static IP ``172.28.7.0``, and ``traefik`` with static IP ``172.28.7.1`` ::
    
    mkdir /opt/portainer
    docker run -d  \
        --restart always \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /opt/portainer:/data \
        --name portainer \
        --hostname portainer \
        --network aqua \
        --ip 172.28.7.0 \
        portainer/portainer
    
    cp -a /etc/pki/tls/certs/localhost.crt /etc/traefik/system.crt
    cp -a /etc/pki/tls/private/localhost.key /etc/traefik/system.key
    docker run -d \
        --restart always \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /etc/traefik:/etc/traefik \
        --name traefik \
        --hostname traefik \
        --network aqua \
        --ip 172.28.7.1 \
        traefik

Access portainer dashboard at ::

    https://IP:980/portainer

Access traefik dashboard at ::

    https://IP:980/traefik

