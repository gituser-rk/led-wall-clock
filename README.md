# led-wall-clock-iobroker
A RGB LED matrix wall clock controlled by a Raspberry Pi.
Modified original project from jeffkub - removed temperature and humidity retrieval from a Internet site and changed to local retrieval from my iobroker smarthome platform. Localisation to Germany: changed the clock format to 24H, temperature to Celsius.
The LOCALE setting of the Raspberry is used for the date display language.
Using the WiFi module of the "RPi Zero W" for the network / Internet connection.
Display color of temperature / humidity is changing depending from their values (values out of "healthy" range --> red color).

![Pic1](pics/IMG_9381.PNG)
![Pic2](pics/IMG_9382.PNG)
![Pic3](pics/IMG_9383.PNG)
![Pic4](pics/IMG_9385.PNG)

# Parts List
- 64x32 RGB LED Matrix - 3mm pitch (https://www.amazon.de/dp/B01ET1QNR4/ref=pe_3044161_185740101_TE_item)
- RPI to HUB75 LED panel adapter kit (http://www.kurokesu.com/shop/led_panels/RPI-HUB75-P-3)
- Raspberry Pi Zero W (https://www.pollin.de/p/raspberry-pi-zero-wh-mit-bestuecktem-header-810885)

# Dependencies
Linux Platform (Raspian Lite)
- NTP client daemon needs to be installed+enabled for automatic time sync.

Python libraries
- [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)
- requests
- apscheduler
- daemonify

ioBroker Adapters (http://www.iobroker.net/)
- iobroker.simple-api 
- iobroker.web (required by simple-api)


# RGB Matrix Library Build Instructions
Clone this repository and submodules to your Raspberry Pi
```
git clone --recursive https://github.com/gituser-rk/led-wall-clock-iobroker.git
cd led-wall-clock-iobroker/rpi-rgb-led-matrix
```
Edit `lib/Makefile` and uncomment the following two DEFINES
```
# Uncomment the following line for Adafruit Matrix HAT gpio mappings.
# If you have an Adafruit HAT ( https://www.adafruit.com/products/2345 ),
# you need to use this option as the HAT swaps pins around that are not
# compatible with the default mapping.
DEFINES+=-DADAFRUIT_RGBMATRIX_HAT

# Uncomment if you want to use the Adafruit HAT with stable PWM timings.
# The newer version of this library allows for much more stable (less flicker)
# output, but it does not work with the Adafruit HAT unless you do a
# simple hardware hack on them:
# connect GPIO 4 (old OE) with 18 (the new OE); there are
# convenient solder holes labeled 4 and 18 on the Adafruit HAT, pretty
# close together.
# Then uncomment the following define and recompile.
DEFINES+=-DADAFRUIT_RGBMATRIX_HAT_PWM
```
Build and install the Python library
```
make build-python
sudo make install-python
```
# Starting the Clock
To start the clock as a daemon
```
cd led-wall-clock-iobroker
sudo ./ledclock.py -d start
```
# To Do
- change value retrieval from "iobroker.simple-api" to mqtt-subscriber
- Move configuration to a separate file
- Implement dimming based on some I2C ambient light sensor
