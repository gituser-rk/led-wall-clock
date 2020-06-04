import threading
import time
import locale
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

locale.setlocale(locale.LC_ALL,'')

class Display(threading.Thread):
    def __init__(self, weather, dimmer):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self._weather = weather
        self._dimmer = dimmer

        # Configure LED matrix driver
	    # RGBMatrix(Rows,Chained,?)
        self._matrix = RGBMatrix(32, 2, 1)
        self._matrix.pwmBits = 11
        self._matrix.brightness = 25

        # Load fonts
        self._font_large = graphics.Font()
        self._font_large.LoadFont("rpi-rgb-led-matrix/fonts/10x20.bdf")
        self._font_small = graphics.Font()
        self._font_small.LoadFont("rpi-rgb-led-matrix/fonts/6x10.bdf")
        self._font_tiny = graphics.Font()
        self._font_tiny.LoadFont("rpi-rgb-led-matrix/fonts/4x6.bdf")

        # Define colors
        self._white = graphics.Color(255, 255, 255)
        self._amber = graphics.Color(200, 50, 0 )
        self._red = graphics.Color(255, 120, 120)
        self._blue = graphics.Color(120, 120, 255)
        self._green = graphics.Color(150, 255, 100)
        self._pink = graphics.Color(255, 0, 120)


    def _draw(self, canvas):
        canvas.Clear()

        graphics.DrawText(canvas, self._font_large, 1, 13, self._white, time.strftime("%H:%M"))
        graphics.DrawText(canvas, self._font_small, 53, 13, self._pink, time.strftime("%S"))

        graphics.DrawText(canvas, self._font_small, 2, 22, self._green, time.strftime("%a %-d %b"))
        #Format to 2 digits and no subdigits
        sTempOutside = "%2.0f" % self._weather.TempOutside
        sTempInside = "%2.0f" % self._weather.TempInside
        #sHumidityOutside = "%2.0f" % self._weather.HumidityOutside
        sHumidityInside = "%2.0f" % self._weather.HumidityInside
        if self._weather.TempOutside > -10.0 and self._weather.TempOutside < 10.0:
		# temperature only one digit: move output to left (reduce space after 'A:'))
		self._posOffset = -7
	else:
		self._posOffset = 0
        graphics.DrawText(canvas, self._font_small, 1, 31, self._amber, "A")
        graphics.DrawText(canvas, self._font_tiny, 6, 31, self._amber, ":")
        graphics.DrawText(canvas, self._font_small, 16+self._posOffset, 31, self._white, sTempOutside)
        graphics.DrawText(canvas, self._font_tiny, 28+self._posOffset, 28, self._white, "o")

        graphics.DrawText(canvas, self._font_small, 39, 31, self._amber, "I")
        graphics.DrawText(canvas, self._font_tiny, 43, 31, self._amber, ":")
	if time.strftime("%S") not in ('09', '19', '29', '39', '49', '59', '08', '18', '28', '38', '48', '58'):
	# show temperature
                if  self._weather.TempInside<20.0 or self._weather.TempInside > 23.4:
                        # red color if not in optimum range
                        self._color_temp = graphics.Color(255, 0, 0)
                else:
                        # optimum range is 20 ... 23 degrees Celsius
                        self._color_temp = graphics.Color(255, 255, 255)

        	graphics.DrawText(canvas, self._font_small, 47, 31, self._color_temp, sTempInside)
        	graphics.DrawText(canvas, self._font_tiny, 59, 28, self._color_temp, "o")
	else:
	# show humidity
		if  self._weather.HumidityInside<40 or self._weather.HumidityInside > 60:
        	# red color if not in optimum range
			self._color_humidity = graphics.Color(255, 0, 0)
        	else:
			# optimum range is 40 ... 60 % 
			self._color_humidity = graphics.Color(255, 255, 255)

        	graphics.DrawText(canvas, self._font_small, 47, 31, self._color_humidity, sHumidityInside)
        	graphics.DrawText(canvas, self._font_small, 59, 31, self._color_humidity, "%")

    def run(self):
        canvas = self._matrix.CreateFrameCanvas()

        while True:
            self._draw(canvas)
            time.sleep(0.05)
            canvas = self._matrix.SwapOnVSync(canvas)
            self._matrix.brightness = self._dimmer.brightness
