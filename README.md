# G213Colors
A script to change the key colors on a Logitech G213 Prodigy Gaming Keyboard.

Please also check out these awesome forks:

[G213Colors GUI](https://github.com/derEisele/G213Colors) - A cool grafical GUI you can use from the main menu

[G213Colors GUI + installation script](https://github.com/JeroenED/G213Colors) - The GUI plus an easy installation script

Thanks to [derEisele](https://github.com/derEisele) and [JeroenED](https://github.com/JeroenED) for creating this!

## What it does
G213Colors lets you set the color(s) and certain effects of the illuminated keys on a G213 keyboard under Linux.

The original Software and Hardware has the following downsides:
* There is no Linux software
* The keyboard does not save the last setting, one has to re-set it every bootup / disconnect
* The keyboard starts up with an annoying color cycle animation
* The original software is unusable with KVM switches

So i decided to reverse engineer their USB protocol and to write my own script to control the keyboard.

G213Colors was built and tested under Linux for the G213 keyboard specifically, but after some adaptation it could potentially be run under other OS'es and used for other Logitech keyboards as well.
Please understand that i do not support any such adaptation, if you want to do it **you are on your own**.

The "Wave" color effect that is available with the Logitech software could not be replicated since it is completely generated in the software by updating the colors every x ms (In contrast to the other effects which run on the keyboard itself). You could generate this effect with a script, but since G213Colors has to detach the kernel driver from one of the G213's interfaces to send data out the multimedia keys would most likely stop working. Unfortunately this is a side effect of the linux driver structure.

## Installation
Either download the [G213Colors.py](https://raw.githubusercontent.com/SebiTimeWaster/G213Colors/master/G213Colors.py) file to a directory of your choosing **_or_** clone this project with git.

### Prerequisites
* [Python](https://www.python.org/) >= 2.4 or 3.x (which is usually already installed)
* [PyUSB](https://github.com/walac/pyusb)
* [RandomColor](https://github.com/davidmerfield/randomColor)

If you run the script as Root (Which is likely) please install the libraries also as root (E.g.: `sudo pip3 install pyusb`, `sudo pip3 install randomcolor`, use only "pip" for Python 2).

Please ignore the pcap directory, i added the pcap files i used for reverse engineering just in case someone wants to work with them. They can be opened with [Wireshark](https://en.wikipedia.org/wiki/Wireshark).

## Usage
For help on how to use G213Colors call the script without any arguments:

```Bash
sudo python G213Colors.py
```

G213Colors needs to be run as root as long as your user doesn't have access privileges for that USB device ([How to do this](http://stackoverflow.com/a/32022908/2948666), please use "046d" as idVendor and "c336" as idProduct).

## Changelog
Changelog v0.3:
* Added feature: Assign random colors to keyboard by using -ra or -rs flag

Changelog v0.2:
* Fixed bug preventing setting all 5 color fields correctly, thanks to @oncecreated for finding this solution!
* Added propper validation of user inputs
* Complete refactoring

Changelog v0.1:
* Initial checkin
