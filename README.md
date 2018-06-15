# Bitnodes Hardware (discontinued)

Thank you for purchasing Bitnodes Hardware!

The Bitnodes Hardware is a low footprint quad-core single-board computer built and configured to operate as a dedicated Bitcoin full node. It puts you in full control of a device that plays a critical role in the Bitcoin peer-to-peer network by verifying and relaying transactions and blocks across the network.

Each unit comes fully assembled and consumes as low as 2.5W during normal operation making the Bitnodes Hardware ideal for 24/7 operation.

## Quickstart Guide
1. Unpack your Bitnodes Hardware.
1. Plug in the power cord and the Ethernet cable.
1. Note down the LAN IP address (`LAN_IP_ADDRESS`) and the WAN IP address (`WAN_IP_ADDRESS`) for your Bitnodes Hardware displayed on the LCD.
1. Using another computer in the same LAN, open the administration page at `http://LAN_IP_ADDRESS:8001` with a web browser.
1. Click on the **ADMINISTRATION** link at the top-right corner of the page.
1. Login using `admin` as the password.
1. Click **CHANGE PASSWORD** to change your password now.
1. Your Bitnodes Hardware will take a couple hours to sync up with the latest blocks from the network.
1. Once synced, your Bitnodes Hardware will start to verify and relay new transactions and blocks.

**WARNING: DO NOT UNPLUG THE POWER CORD FOR YOUR BITNODES HARDWARE BEFORE STOPPING THE BITCOIN CLIENT GRACEFULLY FROM THE ADMINISTRATION PAGE. FAILURE TO STOP THE BITCOIN CLIENT GRACEFULLY WILL RESULT IN ITS DATABASE CORRUPTION WHICH WILL LIKELY REQUIRE FRESH DOWNLOAD OF THE ENTIRE BLOCKCHAIN.**

## Remote Access
SSH is enabled on your Bitnodes Hardware if you need remote shell access from another computer in the same LAN. Login as `bitnodes` with `bitnodes` as the password. Be sure to change the password as soon as you are logged in. `root` password has been removed for security reason. You will need to be logged in as `bitnodes`, which has sudo access, to execute privileged commands.

    $ ssh bitnodes@LAN_IP_ADDRESS
    $ passwd

## Port Forwarding
Port forwarding must be configured on your router to allow incoming connections to your Bitnodes Hardware. Look for **Port Forwarding** page or similar in your router administration page and add the entries as shown in the table below.

Note that the equivalent fields may be named differently depending on the make and model of your router. Be sure to replace `LAN_IP_ADDRESS` with the actual LAN IP address for your Bitnodes Hardware.

| Service Name       | Internal IP Address | Internal Port | External Port |
|--------------------|---------------------|---------------|---------------|
| Public status page | `LAN_IP_ADDRESS`    | 1008          | 1008          |
| Bitcoin client     | `LAN_IP_ADDRESS`    | 8333          | 8333          |

Restart your Bitnodes Hardware from its administration page for the changes to take effect. You should now be able to access the public status page for your Bitnodes Hardware from `http://WAN_IP_ADDRESS:1008`. Enter your `WAN_IP_ADDRESS` in https://getaddr.bitnodes.io/#join-the-network to confirm that your Bitcoin client is accepting incoming connections.

## Help
If you need assistance setting up your Bitnodes Hardware, please send an email to service@bitnodes.io.

## Hardware Features
* Amlogic Quad-Core ARM Cortex-A5 1.5GHz CPU
* Quad-Core ARM Mali-450 MP GPU OpenGL ES 2.0 600MHz
* 1GB DDR3 SDRAM
* Hardware RNG
* Toshiba 8GB eMMC NAND Flash Memory for Operating System
* [Samsung MicroSDXC 128GB EVO Memory Card](http://www.samsung.com/us/computer/memory-storage-accessories/MB-MP128DA/AM) (Model B1 128GB ONLY)
* 3.2-inch TFT LCD
* Gigabit Ethernet (1.8M CAT6 cable included)
* 4 x USB 2.0
* 1 x Micro USB OTG
* 1 x Standard Type-A HDMI
* Serial Console Port (UART)
* IR Receiver
* 5V 2A DC Input (APAC/AU/EU/US compatible)
* Bitnodes Hardware Clear Acrylic Case
* Width: 115mm x Depth: 86mm x Height: 42mm

## Software Features
* Powered by the latest version of Ubuntu operating system
* Latest version of Bitcoin client synced up to the latest block prior to dispatch
* Built-in open source web-based administration interface:
    * Start or stop Bitcoin client
    * Restart or shutdown your Bitnodes Hardware
    * Set or unset bandwidth limit for Bitcoin client
* Public status page with real-time stats for your Bitnodes Hardware

## Security Features
* Minimal base system
* System packages and Bitcoin client are updated automatically
* Root password disabled
* Administration interface is accessible only from private networks
* Hardware RNG enabled to increase system entropy for use by /dev/random
* Bitcoin client compiled without wallet to ensure it operates only as a full node

## Developer Guide
The sections below describe the steps that were taken to configure your Bitnodes Hardware prior to dispatch. These sections are for your reference only. You are NOT required to execute any of the steps below to start your Bitnodes Hardware.

### Ubuntu Setup
Update your system and install required packages.

    $ sudo apt-get update
    $ sudo apt-get -y upgrade
    $ sudo apt-get -y install autoconf build-essential git-core libboost-all-dev libssl-dev libtool pkg-config python-dev redis-server postgresql postgresql-contrib libpq-dev

Update PostgreSQL authentication file to allow localhost access without password prompt.

    $ sudo vi /etc/postgresql/9.3/main/pg_hba.conf

Replace the content of the file with the following.

    # TYPE        DATABASE        USER        ADDRESS        METHOD
    local         all             all                        trust
    host          all             all         127.0.0.1/32   trust
    host          all             all         ::1/128        trust

Create a PostgreSQL user and database for use by the Django project.

    $ sudo -u postgres createuser --superuser --echo bitnodes
    $ createdb bitnodes

Update sudoers file to allow normal user to execute certain privileged commands without password prompt.

    $ sudo visudo

Add the following lines at the end of the file to allow normal user to restart the system and to configure bandwidth limit for the system. Note that tc and iptables are only available on Linux. `console-setup` is required to allow normal user to reload the console setup, e.g. font size, prior to displaying output on the LCD.

    bitnodes ALL=NOPASSWD: /sbin/shutdown
    bitnodes ALL=NOPASSWD: /sbin/tc
    bitnodes ALL=NOPASSWD: /sbin/iptables
    bitnodes ALL=NOPASSWD: /bin/setupcon

Update the last line in the getty file for tty1 to allow normal user to login automatically at /dev/tty1 to allow the LCD to display the status of your Bitnodes Hardware.

    $ sudo vi /etc/init/tty1.conf
    exec /sbin/getty -8 38400 tty1 -a bitnodes

The administration page and the public status page for your Bitnodes Hardware are powered by the same [Django](https://www.djangoproject.com/) project installed inside a virtualenv environment. Install virtualenv and pip to manage Python packages inside the virtualenv environment.

    $ sudo apt-get -y install python-pip
    $ sudo pip install --upgrade pip
    $ sudo pip install --upgrade virtualenv
    $ sudo pip install virtualenvwrapper

    $ vi ~/.profile

Add the following lines at the end of the file.

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
    if [ `/usr/bin/tty` == "/dev/tty1" ]
    then
        /usr/bin/sudo /etc/init.d/console-setup reload > /dev/null 2>&1
        /home/bitnodes/.virtualenvs/hardware/bin/python /home/bitnodes/hardware/lcd.py
    fi

Install Nginx for use as the front-end web server for the Django project.

    $ sudo apt-get -y install nginx

Install Supervisor to manage processes for the Django project.

    $ sudo apt-get -y install supervisor

### Bitcoin Client Installation
Build and install Bitcoin client from source.

    $ cd
    $ git clone https://github.com/bitcoin/bitcoin.git
    $ cd bitcoin
    $ git checkout v0.13.1
    $ ./autogen.sh
    $ ./configure --without-gui --without-miniupnpc --disable-wallet

Reclaim enough memory by stopping all the supervisor processes including the currently running Bitcoin client before starting the build.

    $ workon hardware
    $ ./manage.py supervisor stop all
    $ deactivate

Start the build.

    $ cd ~/bitcoin
    $ make
    $ make check
    $ mkdir -p ~/bin
    $ cp src/bitcoind src/bitcoin-cli ~/bin/

The Bitcoin client will be updated automatically when a new version becomes available. If you wish to update your Bitcoin client manually, you may remove `~/hardware/.current_bitcoind` to disable the automatic update.

    $ rm ~/hardware/.current_bitcoind

Reboot your Bitnodes Hardware to ensure all processes are started normally.

    $ sudo reboot

### Switching Client
Alternative implementation of Bitcoin client such as Bitcoin XT is supported on your Bitnodes Hardware.

    $ sudo apt-get install libcurl4-openssl-dev
    $ cd
    $ git clone https://github.com/bitcoinxt/bitcoinxt.git
    $ cd bitcoinxt
    $ git checkout 0.11B
    $ ./autogen.sh
    $ ./configure --without-gui --without-miniupnpc --disable-wallet

Reclaim enough memory by stopping all the supervisor processes including the currently running Bitcoin client before starting the build.

    $ workon hardware
    $ ./manage.py supervisor stop all
    $ deactivate

Start the build.

    $ cd ~/bitcoinxt
    $ make
    $ make check
    $ mkdir -p ~/bin
    $ cp src/bitcoind src/bitcoin-cli ~/bin/

Automatic update is not available for alternative implementation of Bitcoin client. Remove `~/hardware/.current_bitcoind` to disable the automatic update.

    $ rm ~/hardware/.current_bitcoind

Reboot your Bitnodes Hardware to ensure all processes are started normally.

    $ sudo reboot

### Django Project Installation
The project is currently supported on Linux and Mac OS X with Python 2.7.x. Clone the project into the home directory and run `setup.sh` to bootstrap the project.

    $ cd
    $ sudo rm -rf ~/.cache
    $ git clone https://github.com/ayeowch/bitnodes-hardware.git hardware
    $ cd hardware
    $ source ~/.profile
    $ mkvirtualenv -a "$PWD" hardware
    $ ./setup.sh
    $ echo v0.13.1 > ~/hardware/.current_bitcoind

Register the project's supervisor with system's supervisor.

    $ cd /etc/supervisor/conf.d
    $ sudo ln -s /home/bitnodes/hardware/supervisor.conf hardware.conf
    $ sudo supervisorctl reread
    $ sudo supervisorctl update

Register the project with Nginx so that you can access the administration page from `http://LAN_IP_ADDRESS:8001` and the public status page from `http://LAN_IP_ADDRESS:1008`. Access to the administration page is limited to localhost and private networks only.

    $ cd /etc/nginx/sites-enabled
    $ sudo rm default
    $ sudo ln -s /home/bitnodes/hardware/nginx.conf hardware.conf
    $ sudo service nginx reload

### Django Project Development
If you are not already in the project's virtualenv environment, execute the following command before executing any of the commands shown in this section.

    $ workon hardware

Execute the following command to access the project's shell.

    $ ./manage.py shell

Run tests.

    $ ./manage.py test

Use supervisor to start all the necessary processes. The administration page is available at http://localhost:18001 and the public status page is available at http://localhost:11008.

    $ ./manage.py supervisor

To start or stop Bitcoin client manually using supervisor. The project expects the executable to exist at `~/bin/bitcoind`.

    $ ./manage.py supervisor start hardware-bitcoind
    $ ./manage.py supervisor stop hardware-bitcoind

Execute the following command to run the website locally with the administration page enabled at http://localhost:8000.

    $ NETWORK=private ./manage.py runserver

Execute the following command to run the website locally with the public status page enabled at http://localhost:8000.

    $ ./manage.py runserver

In order to run the project in debug mode, i.e. `settings.DEBUG=True`, bootstrap the project using the following command.

    $ ./setup.sh -d

To start celery without using supervisor.

    $ celery worker -A hardware -B --purge --loglevel=DEBUG --queues=celery,low_prio,update

Execute the following command to monitor all log files written by the project in production mode.

    $ tail -f *.log /tmp/*.log

### Django Project Update
Stable updates are periodically pushed or merged into the master branch. Execute the following commands to update your local copy of the project.

    $ workon hardware
    $ git checkout master
    $ git pull
    $ ./manage.py collectstatic --noinput
    $ ./manage.py migrate
    $ ./manage.py supervisor restart all

Alternatively, you may execute the following commands to recreate the project using the latest commit from the master branch.

    $ workon hardware
    $ ./setup.sh

### Rebuild System
**WARNING: THIS WILL REMOVE THE OPERATING SYSTEM, ALL APPLICATIONS AND THEIR ASSOCIATED DATA ON THE PRIMARY DISK (eMMC) OF YOUR BITNODES HARDWARE. YOU SHOULD ONLY NEED TO REBUILD YOUR SYSTEM IF IT IS NO LONGER BOOTING UP OR YOU HAVE FORGOTTEN THE PASSWORD TO ACCESS YOUR BITNODES HARDWARE.**

If you wish to rebuild the system for your Bitnodes Hardware, you will need a Linux or Mac OS X host system and a Micro SD card reader, such as [Transcend RDF5 USB 3.0 card reader](http://www.transcend-info.com/Products/No-396), to write a new image into the eMMC.

Detach the eMMC from the back of the main board of your Bitnodes Hardware. Attach the eMMC to the eMMC adapter and plug in the adapter into your Micro SD card reader. Plug in the Micro SD card reader into a USB port on your host system. The boot volume on the eMMC should now be mounted on your host system. Confirm this by checking the output of `df` command on your host system.

    $ df -h

Unmount the boot volume as shown in the output of the `df` command, e.g. /dev/disk2s1, and flash the Bitnodes Hardware image into the entire disk of the eMMC, e.g. /dev/rdisk2. `unxz` is available for download from [XZ Utils](http://tukaani.org/xz/).

    $ sudo diskutil unmount /dev/disk2s1
    $ unxz bitnodes-hardware-2016-10-28.img.xz
    $ sudo dd if=bitnodes-hardware-2016-10-28.img of=/dev/rdisk2 bs=1m
    $ sync

A new boot volume on the eMMC will be mounted on your host system after the steps above. Eject the eMMC.

    $ sudo diskutil eject /dev/rdisk2

Attach the eMMC to the back of the main board of your Bitnodes Hardware and power it up. Execute the following commands on your Bitnodes Hardware to update the project with the latest commit from the master branch.

    $ workon hardware
    $ ./setup.sh
