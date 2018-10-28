_Dieses Dokument ist in Englisch verfasst, da es Informationen für Fortgeschrittene enthält._


# Some Quality Assurance

As our boards are botched up, i.e. produced manually, we'll also call it botch assurance.


## General Information

arduino-cli (still beta)
* https://blog.arduino.cc/2018/08/24/announcing-the-arduino-command-line-interface-cli/
* https://github.com/arduino/arduino-cli

RaspberryPi:
* If you are going to build arduino-cli yourself (go) you probably need a Pi with 1 GB of RAM.


## Setup

Raspberry Pi image: Raspbian Stretch Lite
```
Raspbian Stretch Lite
Minimal image based on Debian Stretch
Version: October 2018
Release date: 2018-10-09
Kernel version: 4.14
Release notes: Link
```

`raspi-config`:
* change password
* change hostname (N1) -> {{{ttnulm-ba}}}; ba is fpr botch assurance ;-)
* predictable network interface (N3) -> enable
* locale -> e.g. de_DE.UTF-8 UTF-8
* change keyboard layout
* activate SSH (P2)
* expand filesystem (A1)


If you want to, now is the time to access the pi via SSH:
```
ssh pi@ttnulm-ba.lan
# or:
ssh pi@ttnulmba.local
```

Install packages:
```
sudo apt install byobu
byobu
sudo apt update; sudo apt full-upgrade
sudo apt install vim git python3-pip python3-gpiozero
```

arduino-cli:
```
mkdir -p ~/ba/tmp
cd ~/ba/tmp
wget https://downloads.arduino.cc/arduino-cli/arduino-cli-0.3.1-alpha.preview-linuxarm.tar.bz2
tar xvjf arduino-cli-0.3.1-alpha.preview-linuxarm.tar.bz2
sudo mv arduino-cli-0.3.1-alpha.preview-linuxarm /usr/local/bin/arduino-cli

# we'll need the arduino:avr cores and the LMIC 1.5 library
arduino-cli core update-index
arduino-cli core install arduino:avr
arduino-cli lib install "IBM LMIC framework"
```


## the actual BA

```
mkdir -p ~/ba
cd ~/ba
```

### TTN

* Create app and device.
* Set activation method to ABP and **disable frame counter checks**.


### Arduino

THE BA IS STILL WORK IN PROGRESS, SO THE FOLLOWING PART OF THIS DOCUMENTATION IS NOT FINISHED YET.

Download testing routines, compile and flash:
```
mkdir ...
cd ...
wget ....

cd ..

arduino-cli compile --fqbn arduino:avr:pro:cpu=8MHzatmega328 muenster_hello_world
arduino-cli upload --port /dev/ttyUSB0 --fqbn arduino:avr:pro:cpu=8MHzatmega328 muenster_hello_world
```



== Debugging ==

`arduino-cli board list` should return:
```
FQBN    Port            ID              Board Name
        /dev/ttyUSB0    0403:6001       unknown
```


arduino-cli can not find the board try `lsusb` which should return:
```
Bus 001 Device 004: ID 0403:6001 Future Technology Devices International, Ltd FT232 USB-Serial (UART) IC
```


## Surplus information

_Not needed for BA._

arduino-cli build with go:
```
sudo apt install snapd
sudo reboot

sudo snap install go --classic
go get -u github.com/arduino/arduino-cli
sudo cp /home/pi/go/bin/arduino-cli /usr/local/bin/arduino-cli
```

Arduino IDE (not necessary):
```
wget https://downloads.arduino.cc/arduino-1.8.7-r1-linuxarm.tar.xz
tar xvJf arduino-1.8.7-r1-linuxarm.tar.xz
cd arduino-1.8.7
./arduino-linux-setup.sh pi
sudo reboot
```
