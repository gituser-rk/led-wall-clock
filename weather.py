import logging
import requests
#import json
#from xml.etree import ElementTree
logging.basicConfig(filename='/root/led-wall-clock/weather.log',level=logging.DEBUG)
# URL's
TEMP_URL = "http://172.16.1.90:8087/getPlainValue/hm-rpc.0.HEQ0110761.1.TEMPERATURE/"
TEMP_WZ_URL = "http://172.16.1.90:8087/getPlainValue/hm-rpc.0.OEQ1667692.2.ACTUAL_TEMPERATURE/"
HUMIDITY_WZ_URL = "http://172.16.1.90:8087/getPlainValue/hm-rpc.0.OEQ1667692.2.ACTUAL_HUMIDITY/"

class Weather(object):
    def __init__(self, scheduler, zip, station):
        self._zip = zip
        self._station = station

        self.cur_temp = 0.0
        self.cur_temp_wz = 0.0
        self.high_temp = 0.0
        self.low_temp = 0.0

        self.update()

        # Update every 5 minutes
        scheduler.add_job(self.update, 'cron', minute='*/5')


    def update(self):
        logging.info("Updating ...")
	temp_req = requests.get(TEMP_URL)
	temp_nord = temp_req.text
        temp_wz_req = requests.get(TEMP_WZ_URL)
        temp_wz = temp_wz_req.text
        humidity_wz_req = requests.get(HUMIDITY_WZ_URL)
        humidity_wz = humidity_wz_req.text

	if temp_req.ok:
	    self.cur_temp = float(temp_nord)
            self.cur_temp_wz = float(temp_wz)
            self.cur_humidity_wz = float(humidity_wz)
            logging.info("Current temperature Nord %1.1f" % self.cur_temp)
            logging.info("Current temperature WZ %1.1f" % self.cur_temp_wz)
            logging.info("Current humidity WZ %1.1f" % self.cur_humidity_wz)

