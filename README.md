# led-wall-clock
A RGB LED matrix wall clock controlled by a Raspberry Pi.
Modyfied original project from jeffkub - changed temperature and humidity retrieval from a Internet site to local retrieval from my iobroker smarthome platform. Localisation to German: changed the clock format to 24H, temperature to Celsius.


# Parts List
- [64x32 RGB LED Matrix - 5mm pitch](https://www.adafruit.com/products/2277)
- RPI to HUB75 LED panel adapter kit (http://www.kurokesu.com/shop/led_panels/RPI-HUB75-P-3)
- Raspberry Pi Zero W

# Dependencies
Python libraries
- [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)
- requests
- apscheduler
- daemonify

# RGB Matrix Hat Modification
The brightness can be controlled by pulse-width-modulating the OE pin of the LED matrix.  Unfortunately, the hat does not have the PWM pin of the Raspberry Pi connected to the OE pin.  To correct this, jumper a wire between pins labeled 4 and 18 on the hat.

# RGB Matrix Library Build Instructions
Clone this repository and submodules to your Raspberry Pi
```
git clone --recursive https://github.com/jeffkub/led-wall-clock.git
cd led-wall-clock/rpi-rgb-led-matrix
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
cd led-wall-clock
sudo ./ledclock.py -d start
```
# To Do
- Use a more generic weather API
- Move configuration to a separate file
- Implement dimming based on TSL2591 light sensor
- Add forecast screen (toggle on a timer)
