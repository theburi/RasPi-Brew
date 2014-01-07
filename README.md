RasPi-Brew
==========

Brewing service for Rasbery Pi

Installation:

Python

I2C SUB

* LIGHTTPD
	** sudo apt-get install lighttpd python-flup



	** sudo nano /etc/lighttpd/lighttpd.conf

	1. Add
	server.modules = (
        .....
        "mod_fastcgi",
    )
    2. Add
    fastcgi.server = (
        ".py" => (
                "python-fcgi" => (
                        "socket" => "/tmp/fastcgi.python.socket",
                        "bin-path" => "/var/www/brew/index.py",
                        "check-local" => "disable",
                        "max-procs" => 1)
                )
)

    ** Clone Git into /home/RasPi-Brew

    ** add to nano /etc/modules

        # 1-Wire devices
        w1-gpio
        # 1-Wire thermometer devices
        w1-therm

    ** with Sensor connected check
        cd /sys/bus/w1/devices/
        ls
        A sensor ID must be displayed. take a note of it.
        
    ** configure wirelss Ad-hoc
    auto wlan0
	iface wlan0 inet static
    	address 192.168.1.1
    	netmask 255.255.255.0
    	wireless-channel 1
    	wireless-essid MyNETWORK
    	wireless-mode ad-hoc
    	
    **  sudo cp service.sh /etc/init.d
    	sudo chmod 755 /etc/init.d/service.sh

