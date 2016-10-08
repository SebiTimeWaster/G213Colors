# G213Colors
A script to change the key colors on a Logitech G213 Prodigy Gaming Keyboard.

## What it does
G213Colors lets you set the color(s) and certain effects of the illuminated keys on a G213 keyboard under Linux.

Since Logitech is mostly ignoring the Linux market with their "Logitech Gaming Software" but i wanted to use my expensive new keyboard also under linux without tolerating the color cycling animation all the time i decided to reverse engineer their USB protocol and to write my own script to control the keyboard. 
Also my keyboard is attached to an Aten KVM switch which interferes with the Logitech software to the degree that the computer becomes unusable in the worst case and the software does not start in the best case.

G213Colors was built and tested as a Python script under Linux for the G213 keyboard specifically, but it could potentially be run under other OS'es and used for other Logitech keyboards as well, after some adaptation. 
Please understand that i do not support any such adaptation, if you want to do it **you are on your own**.

The "Wave" color effect that is available with the Logitech software could not be replicated since it is completely generated in the software by updating the colors every x ms (In contrast to the other effects which run on they keyboard itself). You could generate this effect with a script, but since G213Colors has to detach the kernel driver from one of the G213's interfaces to send data out the multimedia keys would most likely stop working. Unfortunately this is a side effect of the linux driver structure.

## Installation
Please ignore the pcap directory, i added the pcap files i used for reverse engineering in case someone wants to use them for more features, they can be opened with [Wireshark](https://en.wikipedia.org/wiki/Wireshark).

Either copy the [G213Colors.py](G213Colors/G213Colors.py) file to a directory of your choosing directly or clone this project with git. 

### Prerequisites
You need at least [Python 2.x](https://www.python.org/) and [PyUSB](https://walac.github.io/pyusb/) which are usually already installed on Debian, Ubuntu and other distributions.

## Usage
G213Colors needs to be run as root as long as you didn't add your own user as a privileged user for that USB device.

G213Colors is designed to be used as a shell script for maximum flexibilty and the syntax is easy and Bash-like.
For help on how to use G213Colors call the script without any arguments:

```Bash
sudo python G213Colors.py
```

## Changelog
Changelog v0.1:
* Initial checkin
