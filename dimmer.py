import ephem
import logging


class Dimmer(object):
    def __init__(self, scheduler):
        self._observer = ephem.Observer()
        self._observer.pressure = 0
        self._observer.horizon = '-6'
	# Falkensee:
        self._observer.lat = '52.562044'
        self._observer.lon = '13.07700030'

        self.brightness = 100

        self.update()

        # Run every 5 minutes
        scheduler.add_job(self.update, 'cron', minute='*/5')

    def update(self):
        self._observer.date = ephem.now()

        morning = self._observer.next_rising(ephem.Sun(), use_center=True)
        night = self._observer.next_setting(ephem.Sun(), use_center=True)

        if morning < night:
            # Morning is sooner, so it must be night
            logging.info("It is night time")
            self.brightness = 10
            #self.brightness = 100
        else:
            logging.info("It is day time")
            self.brightness = 25
            #self.brightness = 100
