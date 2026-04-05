
# Animotion

This repository is part of a wildlife monitoring project.
It uses the Raspberry Pi camera module to record videos.
Recording is governed by detected motion.

## Preliminaries
You'll need a [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-5/) and a [Camera Module](https://www.raspberrypi.com/products/camera-module-v2/).
Get a [NoIR](https://www.raspberrypi.com/products/pi-noir-camera-v2/) camera module or better yet one [assembled with lense and IR flashlights](https://thepihut.com/products/raspberry-pi-night-vision-camera-ir-cut).
Also make sure to have the necessary sd card, cabling, power supply, and additional accessories to our liking at hand.

You'll first have to install the [Raspberry Pi OS](https://www.raspberrypi.com/software/) on your sd card.
You can use their imager or download the most recent [Raspian Image](https://www.raspberrypi.com/software/operating-systems/) and copy it manually onto the sd card.
The Lite version should suffice.
Next, connect the Raspberry Pi to your network and peripherals, plug the sd card, and boot it for the first time.
Go through the setup steps as prompted.
Make sure you'll have a network and internet connection as this will be required for the following instructions.



## Install animotion
Update the system and install preliminaries:

    sudo apt update && sudo apt dist-upgrade
    sudo apt install git virtualenv

Fetch animotion:

    git clone http://github.com/igsor/animotion
    cd animotion

Create a virtual environment, install dependencies:

    sudo ./install_non_python_packages.sh
    virtualenv .venv --system-site-packages
    source .venv/bin/activate
    pip install poetry
    poetry sync

You can now run the animotion recorder.
The following command

    recorder --help


## Run animotion on boot
To start animotion recorder automatically you need to register it with the OS (systemd).
This comes in three steps: First, you need a run script, second a systemd unit specification, third you enable it to be started.

### run script
You already have the run script `run-recorder.sh` in the animotion repository folder.
Two changes may be necessary: Command and paths.

Append the command in `run-recorder.sh` to your needs.
In particular, add the `--vflip` and `--hflip` options to the `recorder` command depending on how you mount the camera.
For example, add the `--vflip` line like below if the camera is mounted upside-down:

    recorder \
        --vflip \
        ...

No path change should be necessary if you followed this readme exactly.
If you installed the animotion repository in a different location you must at least adjust the `ENV_FOLDER` and `OUTPUT_FOLDER` paths:

    ENV_FOLDER="~/animotion/.venv/"
    OUTPUT_FOLDER="~/animotion/output/"

At least note the output paths since that's where images and videos will be dropped!

### systemd unit specification
In `animotion.service`, insert the username you chose during the basic OS setup in the two indicated places. This ensures that animotion will run with the correct permissions.


### enable animotion recorder at boot
Make sure that the run-script is executable:

    chmod "+x" run-recorder.sh

Register the unit with systemd:

    sudo ln -s ~/animotion/animotion.service /etc/systemd/system/animotion.service

Reload systemd:

    systemctl daemon-reload

Start animotion at boot:

    systemctl enable animotion.service



## Configure an Access Point
You'll need to manage your Raspberry Pi while it runs animotion.
At least, you'll have to tune the focus and retrieve images from the sd card.
If you have a Raspberry Pi with Wifi you can do such tasks over the air.
But first, we'll have to configure remote access.
Note that in this process you'll lose your internet connection over wifi.
Make sure that you've finished the animotion installation and confirm that it's running.

### Configure services
First, install three packages:

    sudo apt update && sudo apt dist-upgrade
    sudo apt install hostapd dhcpcd dnsmasq

Next, configure the three services by editing their configuration files.

Add the following lines to the bottom of `/etc/dhcpcd.conf`:

    interface wlan0
    static ip_address=192.168.42.1/24
    nohook wpa_supplicant


Add the following lines to the bottom of `/etc/dnsmasq.conf`:

    interface=wlan0
    dhcp-range=192.168.42.2,192.168.42.100,255.255.255.0,6h


Add the following lines to `/etc/hostapd/hostapd.conf`.
Change the ssid and wpa_passphrase accordingly:

    interface=wlan0
    driver=nl80211
    ssid=<YOUR SSID>
    hw_mode=g
    channel=6
    wmm_enabled=0
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase=<YOUR PASSWORD>
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP

Update the following line in `/etc/defaults/hostapd`:
    DAEMON_CONF="/etc/hostapd/hostapd.conf"

### Enable access point on boot:

First, enable the three services on boot:

    systemctl unmask hostapd dnsmasq dhcpcd
    systemctl enable hostapd dnsmasq dhcpcd

Also, disable the network manager, so that it doesn't connect to a wifi:

    systemctl disable NetworkManager

Note that after these changes you won't be able to easily connect to a wifi for internet after the next reboot.
In such a case, you'll need to temporarily stop the access point and bring the network manager up again:

    systemctl stop hostapd dnsmasq dhcpcd
    systemctl start NetworkManager


### Finalization

When being done with the previous steps you'll be able to connect to the Raspberry Pi's access point.
You'll also need some means to actually log in to it.
You can do this by enabling the ssh service.

While you're at it, you can also tweak the system a bit.

Enter the raspbi config menu:

    sudo raspi-config

Enable the SSH service.
This will allow you to log into the system via `ssh 192.168.42.1` once connected to its access point:

    3 Interface Options -> I1 SSH -> YES

At the same time noone else should be able to use the system without password, so let's disable the auto login:

    1 System Options -> S6 Auto Login -> NO

Since you likely won't have a screen attached, you can also disable the graphical interface:

    1 System Options -> S5 Boot -> B1 Console Text console

Exit the `raspi-config` and reboot to apply all of your canges.
After the reboot you should see a new access point with the SSID you configured.


## Development
To ensure code style discipline, run the following commands:

    $ bash lint.sh

To see test coverage, run (after the above!)

    $ xdg-open .htmlcov/index.html

To build the package, do:

    $ python -m build
